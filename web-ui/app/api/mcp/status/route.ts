import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs';

const execAsync = promisify(exec);

// Check if Cursor MCP is available by attempting to invoke it
export async function GET() {
  try {
    // This is a very simple check - in a production environment,
    // you would do a more thorough check by actually invoking an MCP tool
    
    // Look for .cursor/mcp.json in the project root
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
        available: false,
        message: 'No MCP configuration found',
        details: {
          reason: 'missing_config',
          searchPath: webUiDir
        }
      });
    }
    
    // Parse the MCP config
    const mcpConfig = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf8'));
    
    // Check if there's a godmode server in the config
    const hasGodModeServer = mcpConfig.mcpServers && 
                             mcpConfig.mcpServers.godmode;
    
    if (!hasGodModeServer) {
      return NextResponse.json({
        available: false,
        message: 'God Mode MCP server not configured',
        details: {
          reason: 'missing_server',
          configPath: mcpConfigPath
        }
      });
    }
    
    // This doesn't guarantee MCP is working, just that it's properly configured
    return NextResponse.json({
      available: true,
      message: 'MCP configuration found',
      details: {
        configPath: mcpConfigPath,
        serverType: mcpConfig.mcpServers.godmode.command ? 'stdio' : 'sse'
      }
    });
    
  } catch (error) {
    console.error('Error checking MCP status:', error);
    return NextResponse.json({
      available: false,
      message: 'Error checking MCP status',
      details: {
        error: error instanceof Error ? error.message : String(error)
      }
    });
  }
} 