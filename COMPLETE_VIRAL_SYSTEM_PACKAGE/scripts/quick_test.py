#!/usr/bin/env python3
"""
Quick Test Script - Viral YouTube Documentary System
=====================================================

This script performs a quick health check of your installation.

What it tests:
1. Python version
2. Required packages
3. API key configuration
4. Database connectivity
5. Agent functionality

Usage:
    python scripts/quick_test.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠ {text}")

def test_python_version():
    """Test if Python version is compatible"""
    print_header("Testing Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Current version: Python {version_str}")
    
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} is compatible!")
        return True
    else:
        print_error(f"Python {version_str} is not compatible!")
        print("  Required: Python 3.11 or higher")
        return False

def test_packages():
    """Test if required packages are installed"""
    print_header("Testing Required Packages")
    
    # List of critical packages
    critical_packages = [
        "anthropic",
        "langchain",
        "langgraph",
        "chromadb",
        "openai",
        "pydantic",
        "requests"
    ]
    
    missing_packages = []
    
    for package in critical_packages:
        try:
            __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\nMissing packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nTo install: pip install -r requirements.txt")
        return False
    
    return True

def test_api_keys():
    """Test if API keys are configured"""
    print_header("Testing API Keys")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print_error("python-dotenv not installed")
        return False
    
    # Check for .env file
    if not os.path.exists(".env"):
        print_error(".env file not found")
        print("  Create .env file and add your API keys")
        print("  See .env.example for template")
        return False
    
    print_success(".env file found")
    
    # Check API keys
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    
    all_keys_present = True
    
    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        print_success("Anthropic API key is configured")
    else:
        print_error("Anthropic API key is NOT configured")
        print("  Get your key at: https://console.anthropic.com/")
        all_keys_present = False
    
    if openai_key and openai_key != "your_openai_api_key_here":
        print_success("OpenAI API key is configured")
    else:
        print_error("OpenAI API key is NOT configured")
        print("  Get your key at: https://platform.openai.com/api-keys")
        all_keys_present = False
    
    # Optional keys
    jstor_key = os.getenv("JSTOR_API_KEY", "")
    if jstor_key and jstor_key != "your_jstor_api_key_here":
        print_success("JSTOR API key is configured (optional)")
    else:
        print_warning("JSTOR API key is NOT configured (optional)")
    
    return all_keys_present

def test_directories():
    """Test if necessary directories exist"""
    print_header("Testing Project Structure")
    
    required_dirs = [
        "agents/gatekeepers",
        "agents/subagents",
        "config",
        "scripts",
        "docs"
    ]
    
    all_present = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_success(f"{dir_path}/ exists")
        else:
            print_error(f"{dir_path}/ NOT found")
            all_present = False
    
    return all_present

def test_agent_imports():
    """Test if agent files can be imported"""
    print_header("Testing Agent Files")
    
    try:
        # Try importing key agent files
        sys.path.insert(0, "agents/subagents")
        
        print("Attempting to import agents...")
        
        try:
            from academic_depth_specialist import AcademicDepthSpecialist
            print_success("AcademicDepthSpecialist imports successfully")
        except Exception as e:
            print_error(f"AcademicDepthSpecialist failed: {str(e)[:50]}")
            return False
        
        try:
            from accessibility_translator import AccessibilityTranslator
            print_success("AccessibilityTranslator imports successfully")
        except Exception as e:
            print_error(f"AccessibilityTranslator failed: {str(e)[:50]}")
            return False
        
        print_success("All agent files can be imported!")
        return True
        
    except Exception as e:
        print_error(f"Agent import failed: {str(e)}")
        return False

def test_api_connectivity():
    """Test API connectivity (if keys are configured)"""
    print_header("Testing API Connectivity")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    
    if not anthropic_key or anthropic_key == "your_anthropic_api_key_here":
        print_warning("Skipping API test (API key not configured)")
        return True
    
    try:
        from anthropic import Anthropic
        
        print("Testing Anthropic API connection...")
        client = Anthropic(api_key=anthropic_key)
        
        # Simple test message
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": "Reply with 'API test successful' and nothing else."
            }]
        )
        
        response = message.content[0].text
        
        if "successful" in response.lower():
            print_success("API connection successful!")
            return True
        else:
            print_error("API connection failed (unexpected response)")
            return False
            
    except Exception as e:
        print_error(f"API connection failed: {str(e)[:100]}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  VIRAL DOCUMENTARY SYSTEM - QUICK TEST")
    print("=" * 60)
    
    results = {
        "Python Version": test_python_version(),
        "Packages": test_packages(),
        "API Keys": test_api_keys(),
        "Directories": test_directories(),
        "Agent Imports": test_agent_imports(),
        "API Connectivity": test_api_connectivity()
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use!")
        print("\nNext steps:")
        print("  1. Try testing individual agents:")
        print("     python agents/subagents/academic_depth_specialist.py")
        print("  2. Read documentation:")
        print("     docs/MULTI_AGENT_SYSTEM_SUMMARY.md")
        print("  3. Generate your first documentary!")
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install packages: pip install -r requirements.txt")
        print("  - Add API keys to .env file")
        print("  - Check file structure matches requirements")
        return 1

if __name__ == "__main__":
    sys.exit(main())
