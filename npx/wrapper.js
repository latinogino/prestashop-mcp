#!/usr/bin/env node

const { spawn } = require('child_process');
const { program } = require('commander');
const which = require('which');
const path = require('path');
const fs = require('fs');

program
  .name('prestashop-mcp')
  .description('PrestaShop MCP Server (NPX wrapper for Python version)')
  .version('1.0.0')
  .option('--shop-url <url>', 'PrestaShop shop URL')
  .option('--api-key <key>', 'PrestaShop API key')
  .option('--log-level <level>', 'Logging level', 'INFO')
  .option('--python-path <path>', 'Path to Python prestashop-mcp installation')
  .parse();

const options = program.opts();

async function findPython() {
  const candidates = ['python3', 'python'];
  
  for (const candidate of candidates) {
    try {
      await which(candidate);
      return candidate;
    } catch (error) {
      continue;
    }
  }
  
  throw new Error('Python not found. Please install Python 3.8+');
}

async function findPrestashopMcp() {
  // Option 1: User-specified path
  if (options.pythonPath) {
    return options.pythonPath;
  }
  
  // Option 2: Look for local installation relative to this NPX wrapper
  const localPath = path.resolve(__dirname, '..', 'src');
  if (fs.existsSync(path.join(localPath, 'prestashop_mcp'))) {
    return localPath;
  }
  
  // Option 3: Use installed Python package
  return null;
}

async function main() {
  try {
    const python = await findPython();
    const pythonPath = await findPrestashopMcp();
    
    // Build arguments for Python CLI
    const args = ['-m', 'prestashop_mcp.cli'];
    
    if (options.shopUrl) {
      args.push('--shop-url', options.shopUrl);
    }
    
    if (options.apiKey) {
      args.push('--api-key', options.apiKey);
    }
    
    if (options.logLevel) {
      args.push('--log-level', options.logLevel);
    }

    console.log('🔄 Launching Python PrestaShop MCP Server via NPX...');
    
    // Prepare environment
    const env = {
      ...process.env,
      PRESTASHOP_SHOP_URL: options.shopUrl || process.env.PRESTASHOP_SHOP_URL,
      PRESTASHOP_API_KEY: options.apiKey || process.env.PRESTASHOP_API_KEY,
      LOG_LEVEL: options.logLevel || process.env.LOG_LEVEL
    };
    
    // Add PYTHONPATH if local installation found
    if (pythonPath) {
      env.PYTHONPATH = pythonPath + (env.PYTHONPATH ? path.delimiter + env.PYTHONPATH : '');
      console.log(`📂 Using local Python path: ${pythonPath}`);
    }
    
    // Spawn Python process
    const child = spawn(python, args, {
      stdio: 'inherit',
      env: env
    });

    child.on('exit', (code) => {
      process.exit(code || 0);
    });

    child.on('error', (error) => {
      console.error('❌ Failed to start Python process:', error.message);
      console.error('💡 Make sure Python and prestashop-mcp are installed');
      process.exit(1);
    });

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error('💡 Try: npm install -g . (from the npx directory)');
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };