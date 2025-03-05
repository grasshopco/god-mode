import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs';
import { spawn } from 'child_process';

const execAsync = promisify(exec);

// Invoke MCP tools
export async function POST(request: Request) {
  try {
    const { tool, parameters } = await request.json();
    
    if (!tool || typeof tool !== 'string') {
      return NextResponse.json({ error: 'Invalid or missing tool name' }, { status: 400 });
    }
    
    // Only allow specific tools for security reasons
    const allowedTools = [
      'god_mode.enhance',
      'god_mode.process',
      'god_mode.memory',
      'god_mode.route'
    ];
    
    if (!allowedTools.includes(tool)) {
      return NextResponse.json({
        error: 'Unsupported tool',
        message: `Tool '${tool}' is not supported. Allowed tools: ${allowedTools.join(', ')}`
      }, { status: 400 });
    }
    
    // Find the God Mode directory
    const webUiDir = process.cwd();
    let currentDir = webUiDir;
    let mcpConfigPath = null;
    
    // Check parent directories for .cursor/mcp.json
    while (currentDir !== path.parse(currentDir).root) {
      const possiblePath = path.join(currentDir, '.cursor', 'mcp.json');
      if (fs.existsSync(possiblePath)) {
        mcpConfigPath = possiblePath;
        break;
      }
      currentDir = path.resolve(currentDir, '..');
    }
    
    if (!mcpConfigPath) {
      return NextResponse.json({
        error: 'MCP not configured',
        message: 'No MCP configuration found'
      }, { status: 500 });
    }
    
    // Parse the MCP config
    const mcpConfig = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
    
    // Check if there's a godmode server in the config
    const mcpServer = mcpConfig.mcpServers && mcpConfig.mcpServers.godmode;
    
    if (!mcpServer) {
      return NextResponse.json({
        error: 'God Mode MCP server not configured',
        message: 'The God Mode MCP server is not configured in the MCP configuration'
      }, { status: 500 });
    }
    
    // Determine the command to run the MCP server
    let command: string;
    let args: string[] = [];
    
    if (mcpServer.command) {
      // It's a stdio server
      command = mcpServer.command;
      
      if (mcpServer.args) {
        args = mcpServer.args.map((arg: string) => {
          // Replace ${workspaceRoot} with the actual directory
          if (typeof arg === 'string') {
            return arg.replace('${workspaceRoot}', path.dirname(path.dirname(mcpConfigPath)));
          }
          return arg;
        });
      }
    } else {
      return NextResponse.json({
        error: 'Unsupported MCP server type',
        message: 'Only stdio MCP servers are supported at this time'
      }, { status: 500 });
    }
    
    // Prepare the MCP request
    const mcpRequest = {
      type: 'execute',
      name: tool,
      parameters: parameters || {}
    };
    
    // Spawn the MCP server process
    const mcpProcess = spawn(command, args, {
      cwd: path.dirname(path.dirname(mcpConfigPath)) // Workspace root
    });
    
    // Send the request to the MCP server
    mcpProcess.stdin.write(JSON.stringify(mcpRequest) + '\n');
    mcpProcess.stdin.end();
    
    // Collect the response
    let responseData = '';
    mcpProcess.stdout.on('data', (data) => {
      responseData += data.toString();
    });
    
    // Collect errors
    let errorData = '';
    mcpProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`MCP stderr: ${data}`);
    });
    
    // Return the response when the process exits
    return new Promise((resolve) => {
      mcpProcess.on('close', (code) => {
        if (code !== 0) {
          console.error(`MCP process exited with code ${code}`);
          console.error(`Error output: ${errorData}`);
          
          resolve(NextResponse.json({
            error: 'MCP process failed',
            message: `MCP process exited with code ${code}`,
            stderr: errorData
          }, { status: 500 }));
          return;
        }
        
        try {
          // Parse the response
          const response = JSON.parse(responseData.trim());
          
          if (response.error) {
            resolve(NextResponse.json({
              error: 'MCP tool error',
              message: response.error
            }, { status: 500 }));
            return;
          }
          
          resolve(NextResponse.json({
            success: true,
            result: response.result,
            tool: tool
          }));
        } catch (error) {
          console.error('Error parsing MCP response:', error);
          console.error('Raw response:', responseData);
          
          resolve(NextResponse.json({
            error: 'Invalid MCP response',
            message: 'The MCP server returned an invalid response',
            raw: responseData
          }, { status: 500 }));
        }
      });
    });
    
  } catch (error) {
    console.error('Error invoking MCP tool:', error);
    return NextResponse.json({ 
      error: 'Failed to invoke MCP tool', 
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
} 