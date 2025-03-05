import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs';

const execAsync = promisify(exec);

// Find the GOD_MODE_PROJECT_STARTER_TEMPLATE directory
const findGodModeDir = async () => {
  // Start from the current directory and go up until we find god_mode
  const webUiDir = process.cwd();
  let currentDir = webUiDir;
  
  // Try the parent directory first (common case)
  const parentDir = path.resolve(currentDir, '..');
  if (fs.existsSync(path.join(parentDir, 'god_mode'))) {
    return parentDir;
  }
  
  // If not found, look for god_mode in the current directory or parents
  while (currentDir !== path.parse(currentDir).root) {
    if (fs.existsSync(path.join(currentDir, 'god_mode'))) {
      return currentDir;
    }
    currentDir = path.resolve(currentDir, '..');
  }
  
  throw new Error('Could not find God Mode directory');
};

export async function POST(request: Request) {
  try {
    const { aiResponse, prompt } = await request.json();
    
    if (!aiResponse || typeof aiResponse !== 'string') {
      return NextResponse.json({ error: 'Invalid AI response' }, { status: 400 });
    }
    
    // Find the God Mode directory
    const godModeDir = await findGodModeDir();
    const godModeScriptsDir = path.join(godModeDir, 'god_mode', 'scripts');
    
    // Check if the scripts directory exists
    if (!fs.existsSync(godModeScriptsDir)) {
      return NextResponse.json({ error: 'God Mode scripts directory not found' }, { status: 500 });
    }
    
    // Create a temporary file for the AI response
    const tempResponseFile = path.join(godModeDir, 'temp_ai_response.txt');
    fs.writeFileSync(tempResponseFile, aiResponse);
    
    try {
      // Check if the script_auto_commit.sh exists
      const scriptPath = path.join(godModeScriptsDir, 'script_auto_commit.sh');
      if (!fs.existsSync(scriptPath)) {
        return NextResponse.json({ error: 'Auto commit script not found' }, { status: 500 });
      }
      
      // Make sure the script is executable
      await execAsync(`chmod +x ${scriptPath}`);
      
      // Execute the script and pass the AI response
      const cmd = `cd ${godModeDir} && cat "${tempResponseFile}" | ${scriptPath}`;
      const { stdout, stderr } = await execAsync(cmd);
      
      if (stderr && !stderr.includes('Already up to date')) {
        console.warn('Script warnings:', stderr);
      }
      
      // Define proper types for the results
      interface ProcessResults {
        success: boolean;
        message: string;
        details: string;
        logs: string[];
        memoryUpdates: string[];
        filesToCommit: string[];
      }
      
      // Parse the results from stdout
      const results: ProcessResults = {
        success: true,
        message: 'Response processed successfully',
        details: stdout,
        logs: [],
        memoryUpdates: [],
        filesToCommit: []
      };
      
      // Extract useful information from stdout if available
      if (stdout) {
        // Try to extract logs and memory updates
        const logMatch = stdout.match(/Log saved to: (.+)/g);
        if (logMatch) {
          results.logs = logMatch.map(m => m.replace('Log saved to: ', '').trim());
        }
        
        const memoryMatch = stdout.match(/Memory updated: (.+)/g);
        if (memoryMatch) {
          results.memoryUpdates = memoryMatch.map(m => m.replace('Memory updated: ', '').trim());
        }
        
        const commitMatch = stdout.match(/Committing file: (.+)/g);
        if (commitMatch) {
          results.filesToCommit = commitMatch.map(m => m.replace('Committing file: ', '').trim());
        }
      }
      
      return NextResponse.json(results);
    } finally {
      // Clean up temporary file
      if (fs.existsSync(tempResponseFile)) {
        fs.unlinkSync(tempResponseFile);
      }
    }
  } catch (error) {
    console.error('Error processing response:', error);
    return NextResponse.json({ 
      error: 'Failed to process response', 
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
} 