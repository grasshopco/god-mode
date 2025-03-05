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
    const { prompt } = await request.json();
    
    if (!prompt || typeof prompt !== 'string') {
      return NextResponse.json({ error: 'Invalid prompt' }, { status: 400 });
    }
    
    // Find the God Mode directory
    const godModeDir = await findGodModeDir();
    const godModeScriptsDir = path.join(godModeDir, 'god_mode', 'scripts');
    
    // Check if the scripts directory exists
    if (!fs.existsSync(godModeScriptsDir)) {
      return NextResponse.json({ error: 'God Mode scripts directory not found' }, { status: 500 });
    }
    
    // Create a temporary file for the prompt
    const tempPromptFile = path.join(godModeDir, 'temp_prompt.txt');
    fs.writeFileSync(tempPromptFile, prompt);
    
    // Temporary file for enhanced prompt
    const tempEnhancedFile = path.join(godModeDir, 'temp_enhanced_prompt.txt');
    
    try {
      // Run the script_prepare_response.sh script first
      await execAsync(`cd ${godModeScriptsDir} && ./script_prepare_response.sh`);
      
      // Run script_enhance_prompt.py to enhance the prompt
      const enhanceScript = path.join(godModeScriptsDir, 'script_enhance_prompt.py');
      const enhanceCmd = `cd ${godModeDir} && python3 ${enhanceScript} "${tempPromptFile}" "${tempEnhancedFile}"`;
      
      await execAsync(enhanceCmd);
      
      // Read the enhanced prompt from the output file
      let enhancedPrompt = '';
      if (fs.existsSync(tempEnhancedFile)) {
        enhancedPrompt = fs.readFileSync(tempEnhancedFile, 'utf8');
      } else {
        // Fallback - use the original prompt if enhancement failed
        enhancedPrompt = prompt + "\n\n[Note: Prompt enhancement failed - using original prompt]";
      }
      
      return NextResponse.json({ enhancedPrompt });
    } finally {
      // Clean up temporary files
      if (fs.existsSync(tempPromptFile)) {
        fs.unlinkSync(tempPromptFile);
      }
      if (fs.existsSync(tempEnhancedFile)) {
        fs.unlinkSync(tempEnhancedFile);
      }
    }
  } catch (error) {
    console.error('Error enhancing prompt:', error);
    return NextResponse.json({ 
      error: 'Failed to enhance prompt', 
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
} 