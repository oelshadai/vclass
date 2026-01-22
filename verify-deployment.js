#!/usr/bin/env node
/**
 * Deployment Verification Script
 * Checks if frontend and backend are properly configured and connected
 */

const axios = require('axios');

const BACKEND_URL = 'https://school-report-saas.onrender.com';
const FRONTEND_URL = 'https://elitetechreport.netlify.app';

async function checkBackend() {
  console.log('🔍 Checking backend health...');
  
  try {
    // Check health endpoint
    const healthResponse = await axios.get(`${BACKEND_URL}/api/health/`, {
      timeout: 10000
    });
    
    if (healthResponse.status === 200) {
      console.log('✅ Backend health check: PASSED');
      console.log(`   Status: ${healthResponse.data.status}`);
    }
    
    // Check CORS
    const corsResponse = await axios.get(`${BACKEND_URL}/api/cors-test/`, {
      timeout: 10000,
      headers: {
        'Origin': FRONTEND_URL
      }
    });
    
    if (corsResponse.status === 200) {
      console.log('✅ CORS configuration: WORKING');
    }
    
    return true;
  } catch (error) {
    console.log('❌ Backend check failed:', error.message);
    return false;
  }
}

async function checkFrontend() {
  console.log('🔍 Checking frontend deployment...');
  
  try {
    const response = await axios.get(FRONTEND_URL, {
      timeout: 10000
    });
    
    if (response.status === 200) {
      console.log('✅ Frontend deployment: ACCESSIBLE');
      
      // Check if manifest is accessible
      const manifestResponse = await axios.get(`${FRONTEND_URL}/manifest.webmanifest`);
      if (manifestResponse.status === 200) {
        console.log('✅ PWA manifest: ACCESSIBLE');
      }
      
      return true;
    }
  } catch (error) {
    console.log('❌ Frontend check failed:', error.message);
    return false;
  }
}

async function checkApiConnectivity() {
  console.log('🔍 Checking API connectivity from frontend perspective...');
  
  try {
    // Simulate a frontend API call
    const response = await axios.get(`${BACKEND_URL}/api/`, {
      timeout: 10000,
      headers: {
        'Origin': FRONTEND_URL,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.status === 200) {
      console.log('✅ API connectivity: WORKING');
      console.log(`   API Version: ${response.data.version}`);
      return true;
    }
  } catch (error) {
    console.log('❌ API connectivity failed:', error.message);
    return false;
  }
}

async function main() {
  console.log('🚀 Starting deployment verification...\n');
  
  const backendOk = await checkBackend();
  console.log('');
  
  const frontendOk = await checkFrontend();
  console.log('');
  
  const apiOk = await checkApiConnectivity();
  console.log('');
  
  if (backendOk && frontendOk && apiOk) {
    console.log('🎉 Deployment verification: ALL CHECKS PASSED');
    console.log('✅ Your application is ready for production use!');
    process.exit(0);
  } else {
    console.log('⚠️  Deployment verification: SOME CHECKS FAILED');
    console.log('❌ Please review the failed checks above');
    process.exit(1);
  }
}

main().catch(error => {
  console.error('💥 Verification script failed:', error.message);
  process.exit(1);
});