"""
Multi-LLM Manager with Load Balancing and Rate Limit Bypass
Supports multiple API keys and providers with automatic failover
"""

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

import os
import random
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import threading
from collections import defaultdict

@dataclass
class LLMConfig:
    """Configuration for an LLM provider"""
    name: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    max_tokens: int = 4000
    rate_limit_per_minute: int = 6000
    provider: str = "groq"  # groq, openai, gemini, anthropic, kimi

class LLMManager:
    """
    Manages multiple LLM providers with load balancing and rate limiting
    """
    
    def __init__(self):
        self.configs: List[LLMConfig] = []
        self.usage_tracker = defaultdict(list)  # Track usage per config
        self.lock = threading.Lock()
        self.current_index = 0
        
    def add_config(self, config: LLMConfig):
        """Add an LLM configuration"""
        self.configs.append(config)
        print(f"✅ Added LLM config: {config.name} ({config.provider}) - {config.model}")
    
    def load_from_env(self):
        """Load LLM configurations from environment variables"""
        
        # Groq configurations
        groq_keys = []
        for i in range(1, 11):  # Support up to 10 Groq keys
            key_name = f"GROQ_API_KEY_{i}" if i > 1 else "GROQ_API_KEY"
            key = os.getenv(key_name)
            if key:
                groq_keys.append(key)
        
        for i, key in enumerate(groq_keys, 1):
            self.add_config(LLMConfig(
                name=f"Groq-{i}",
                model="groq/llama-3.1-8b-instant",
                api_key=key,
                rate_limit_per_minute=6000,
                provider="groq"
            ))
        
        # OpenAI configurations
        openai_keys = []
        for i in range(1, 6):  # Support up to 5 OpenAI keys
            key_name = f"OPENAI_API_KEY_{i}" if i > 1 else "OPENAI_API_KEY"
            key = os.getenv(key_name)
            if key:
                openai_keys.append(key)
        
        for i, key in enumerate(openai_keys, 1):
            self.add_config(LLMConfig(
                name=f"OpenAI-{i}",
                model="gpt-4o-mini",
                api_key=key,
                rate_limit_per_minute=30000,  # Much higher limit
                provider="openai"
            ))
        
        # Gemini configurations - Using Gemma 2 2B model as requested
        gemini_keys = []
        for i in range(1, 6):  # Support up to 5 Gemini keys
            key_name = f"GEMINI_API_KEY_{i}" if i > 1 else "GEMINI_API_KEY"
            key = os.getenv(key_name)
            if key:
                gemini_keys.append(key)
        
        for i, key in enumerate(gemini_keys, 1):
            self.add_config(LLMConfig(
                name=f"Gemini-{i}",
                model="gemini/gemma-3n-e2b-it",  # Using Gemma 2 2B model as requested
                api_key=key,
                rate_limit_per_minute=15000,
                provider="gemini"
            ))
        
        # Anthropic configurations
        anthropic_keys = []
        for i in range(1, 6):  # Support up to 5 Anthropic keys
            key_name = f"ANTHROPIC_API_KEY_{i}" if i > 1 else "ANTHROPIC_API_KEY"
            key = os.getenv(key_name)
            if key:
                anthropic_keys.append(key)
        
        for i, key in enumerate(anthropic_keys, 1):
            self.add_config(LLMConfig(
                name=f"Anthropic-{i}",
                model="claude-3-haiku-20240307",
                api_key=key,
                rate_limit_per_minute=10000,
                provider="anthropic"
            ))
        
        # Kimi configurations - Enhanced support
        kimi_keys = []
        for i in range(1, 6):  # Support up to 5 Kimi keys
            key_name = f"KIMI_API_KEY_{i}" if i > 1 else "KIMI_API_KEY"
            key = os.getenv(key_name)
            if key:
                kimi_keys.append(key)
        
        for i, key in enumerate(kimi_keys, 1):
            self.add_config(LLMConfig(
                name=f"Kimi-{i}",
                model="moonshot-v1-8k",  # Kimi/Moonshot model
                api_key=key,
                base_url="https://api.moonshot.cn/v1",  # Kimi API endpoint
                rate_limit_per_minute=5000,
                provider="kimi"
            ))
        
        print(f"🚀 Loaded {len(self.configs)} LLM configurations")
        return len(self.configs) > 0
    
    def _is_rate_limited(self, config: LLMConfig) -> bool:
        """Check if a config is currently rate limited"""
        with self.lock:
            now = time.time()
            # Remove old usage records (older than 1 minute)
            self.usage_tracker[config.name] = [
                timestamp for timestamp in self.usage_tracker[config.name]
                if now - timestamp < 60
            ]
            
            # Check if we're near the rate limit
            usage_count = len(self.usage_tracker[config.name])
            return usage_count >= (config.rate_limit_per_minute * 0.8)  # 80% of limit
    
    def _record_usage(self, config: LLMConfig):
        """Record usage for rate limiting"""
        with self.lock:
            self.usage_tracker[config.name].append(time.time())
    
    def get_best_config(self) -> Optional[LLMConfig]:
        """Get the best available LLM configuration"""
        if not self.configs:
            return None
        
        # First, try to find a non-rate-limited config
        available_configs = [
            config for config in self.configs
            if not self._is_rate_limited(config)
        ]
        
        if available_configs:
            # Prefer higher-tier providers (OpenAI > Gemini > Anthropic > Groq > Kimi)
            priority_order = ["openai", "gemini", "anthropic", "groq", "kimi"]
            
            for provider in priority_order:
                provider_configs = [c for c in available_configs if c.provider == provider]
                if provider_configs:
                    # Round-robin within the same provider
                    return random.choice(provider_configs)
        
        # If all are rate limited, return the one with the least recent usage
        return min(self.configs, key=lambda c: len(self.usage_tracker[c.name]))
    
    def get_litellm_config(self) -> Dict[str, Any]:
        """Get configuration for LiteLLM"""
        config = self.get_best_config()
        if not config:
            raise Exception("No LLM configurations available")
        
        self._record_usage(config)
        
        # Set environment variable for the selected API key
        if config.provider == "groq":
            os.environ["GROQ_API_KEY"] = config.api_key
        elif config.provider == "openai":
            os.environ["OPENAI_API_KEY"] = config.api_key
        elif config.provider == "gemini":
            os.environ["GEMINI_API_KEY"] = config.api_key
        elif config.provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = config.api_key
        elif config.provider == "kimi":
            os.environ["MOONSHOT_API_KEY"] = config.api_key  # Kimi uses MOONSHOT_API_KEY
        
        print(f"🔄 Using LLM: {config.name} ({config.model})")
        
        llm_config = {
            "model": config.model,
            "api_key": config.api_key,
            "max_tokens": config.max_tokens,
            "temperature": 0.1,
        }
        
        # Add base_url for Kimi
        if config.base_url:
            llm_config["base_url"] = config.base_url
        
        return llm_config
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all LLM configurations"""
        status = {
            "total_configs": len(self.configs),
            "configs": []
        }
        
        for config in self.configs:
            usage_count = len(self.usage_tracker[config.name])
            is_limited = self._is_rate_limited(config)
            
            status["configs"].append({
                "name": config.name,
                "provider": config.provider,
                "model": config.model,
                "usage_last_minute": usage_count,
                "rate_limit": config.rate_limit_per_minute,
                "is_rate_limited": is_limited,
                "utilization": f"{(usage_count / config.rate_limit_per_minute) * 100:.1f}%"
            })
        
        return status

# Global instance
llm_manager = LLMManager()

def initialize_llm_manager():
    """Initialize the LLM manager with configurations from environment"""
    success = llm_manager.load_from_env()
    if not success:
        print("⚠️  No LLM configurations found in environment variables")
        print("Please add API keys to your .env file")
    return success

def get_dynamic_llm_config():
    """Get the best available LLM configuration"""
    return llm_manager.get_litellm_config()

def get_llm_status():
    """Get status of all LLM configurations"""
    return llm_manager.get_status()