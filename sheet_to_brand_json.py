#!/usr/bin/env python3
"""
Excel to Brand JSON Converter
Converts Google Sheets/Excel file with brand configurations to individual JSON files
for the Multi-Brand GPT Validator system.
"""

import pandas as pd
import json
import os
import argparse
from typing import Dict, List, Any, Optional
import warnings

warnings.filterwarnings('ignore')

class BrandConfigConverter:
    def __init__(self, excel_file: str, output_dir: str = "config"):
        self.excel_file = excel_file
        self.output_dir = output_dir
        self.brands = []
        self.platforms = []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
    def load_excel_data(self):
        """Load all sheets from the Excel file"""
        print(f"Loading Excel file: {self.excel_file}")
        
        try:
            # Read all sheet names
            excel_file = pd.ExcelFile(self.excel_file)
            sheet_names = excel_file.sheet_names
            print(f"Found sheets: {sheet_names}")
            
            self.sheets = {}
            for sheet_name in sheet_names:
                try:
                    df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
                    self.sheets[sheet_name] = df
                    print(f"✓ Loaded sheet '{sheet_name}' ({len(df)} rows)")
                except Exception as e:
                    print(f"⚠ Warning: Could not load sheet '{sheet_name}': {e}")
                    
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            raise
            
    def extract_brands_and_platforms(self):
        """Extract brand names and platform names from the sheets"""
        # Try to find brands from different possible sheet structures
        brands_found = set()
        platforms_found = set()
        
        # Look for brands in various sheets
        for sheet_name, df in self.sheets.items():
            if df.empty:
                continue
                
            # Check if this looks like a brand/platform matrix
            if any(col.lower() in ['instagram', 'linkedin', 'tiktok', 'x', 'facebook', 'youtube'] for col in df.columns):
                platforms_found.update([col for col in df.columns if col.lower() in [
                    'instagram', 'linkedin', 'tiktok', 'x', 'facebook', 'youtube', 
                    'pinterest', 'threads', 'reddit', 'quora', 'glassdoor', 'indeed'
                ]])
                
                # Brands might be in the first column or index
                if len(df) > 0:
                    if df.index.name and df.index.name.lower() not in ['unnamed: 0']:
                        brands_found.add(df.index.name)
                    for idx in df.index[:10]:  # Check first 10 rows
                        if isinstance(idx, str) and idx.lower() not in ['unnamed: 0', 'nan']:
                            brands_found.add(idx)
                            
            # Check first column for brand names
            if len(df.columns) > 0:
                first_col = df.iloc[:, 0]
                for val in first_col.dropna().head(10):
                    if isinstance(val, str) and val.lower() not in ['unnamed: 0', 'nan', 'brand', 'platform']:
                        brands_found.add(val)
        
        # Clean up brands and platforms
        self.brands = sorted([b for b in brands_found if b and len(b) > 1])
        self.platforms = sorted([p for p in platforms_found if p])
        
        # Default platforms if none found
        if not self.platforms:
            self.platforms = ["Instagram", "LinkedIn", "TikTok", "X", "Facebook", "YouTube", 
                            "Pinterest", "Threads", "Reddit", "Quora", "Glassdoor", "Indeed"]
        
        # Default brands if none found
        if not self.brands:
            self.brands = ["Amar", "Cilkroad", "Techcycle", "Buyitback", "Pax", "Alogroup", "Silkroad"]
            
        print(f"Detected brands: {self.brands}")
        print(f"Detected platforms: {self.platforms}")
        
    def get_sheet_data(self, sheet_name: str) -> Optional[pd.DataFrame]:
        """Get data from a specific sheet"""
        return self.sheets.get(sheet_name)
        
    def extract_brand_voice(self, brand: str) -> Dict[str, str]:
        """Extract brand voice (tone and style)"""
        voice = {"tone": "Professional, engaging, customer-focused.", "style": "Clear, concise, value-driven."}
        
        # Look for voice data in various sheets
        for sheet_name, df in self.sheets.items():
            if 'voice' in sheet_name.lower() or 'tone' in sheet_name.lower():
                # Try to find brand-specific voice data
                for idx, row in df.iterrows():
                    if isinstance(idx, str) and brand.lower() in idx.lower():
                        if 'tone' in df.columns:
                            voice['tone'] = str(row.get('tone', voice['tone']))
                        if 'style' in df.columns:
                            voice['style'] = str(row.get('style', voice['style']))
                        break
                        
        return voice
        
    def extract_brand_story(self, brand: str) -> str:
        """Extract brand story"""
        story = f"{brand} is committed to delivering exceptional value and service to our customers."
        
        # Look for story data
        for sheet_name, df in self.sheets.items():
            if 'story' in sheet_name.lower() or 'brand' in sheet_name.lower():
                for idx, row in df.iterrows():
                    if isinstance(idx, str) and brand.lower() in idx.lower():
                        if 'story' in df.columns:
                            story = str(row.get('story', story))
                        break
                        
        return story
        
    def extract_platform_enabled(self, brand: str) -> List[str]:
        """Extract which platforms are enabled for this brand"""
        enabled_platforms = []
        
        # Look for platform matrix
        for sheet_name, df in self.sheets.items():
            if any(p.lower() in sheet_name.lower() for p in ['brand', 'platform', 'matrix']):
                # Check if this is a brand x platform matrix
                if any(col.lower() in [p.lower() for p in self.platforms] for col in df.columns):
                    for idx, row in df.iterrows():
                        if isinstance(idx, str) and brand.lower() in idx.lower():
                            for platform in self.platforms:
                                col_name = None
                                for col in df.columns:
                                    if platform.lower() in col.lower():
                                        col_name = col
                                        break
                                        
                                if col_name and pd.notna(row.get(col_name)):
                                    val = row.get(col_name)
                                    # Check if it's enabled (True, 1, "yes", "enabled", etc.)
                                    if (isinstance(val, bool) and val) or \
                                       (isinstance(val, (int, float)) and val > 0) or \
                                       (isinstance(val, str) and val.lower() in ['true', 'yes', 'enabled', '1']):
                                        enabled_platforms.append(platform)
                            break
                            
        # If no specific data found, enable common platforms
        if not enabled_platforms:
            enabled_platforms = ["Instagram", "LinkedIn", "TikTok", "X"]
            
        return enabled_platforms
        
    def extract_cadence(self, brand: str) -> Dict[str, int]:
        """Extract posting cadence (posts per week)"""
        cadence = {}
        
        for sheet_name, df in self.sheets.items():
            if 'cadence' in sheet_name.lower() or 'frequency' in sheet_name.lower():
                for idx, row in df.iterrows():
                    if isinstance(idx, str) and brand.lower() in idx.lower():
                        for platform in self.platforms:
                            col_name = None
                            for col in df.columns:
                                if platform.lower() in col.lower():
                                    col_name = col
                                    break
                                    
                            if col_name and pd.notna(row.get(col_name)):
                                val = row.get(col_name)
                                if isinstance(val, (int, float)):
                                    cadence[platform] = int(val)
                                elif isinstance(val, str) and val.isdigit():
                                    cadence[platform] = int(val)
                        break
                        
        # Default cadence if not found
        for platform in self.platforms:
            if platform not in cadence:
                cadence[platform] = 0
                
        return cadence
        
    def extract_media_policy(self) -> Dict[str, Dict[str, Any]]:
        """Extract media policy for all platforms"""
        media_policy = {}
        
        # Default media policies
        default_policies = {
            "Instagram": {"allowed": ["single_image", "carousel", "reel"], "max_carousel": 10, 
                         "min_res": "1080x1080", "aspect": ["1:1", "4:5", "9:16"], "video_cap": "≤90s"},
            "LinkedIn": {"allowed": ["single_image", "document", "video"], "doc_pages_max": 20, 
                        "min_res": "1200x1200", "aspect": ["1:1", "16:9"], "video_cap": "≤10m"},
            "TikTok": {"allowed": ["short_video"], "min_res": "1080x1920", 
                      "aspect": ["9:16"], "video_cap": "≤60s"},
            "X": {"allowed": ["single_image", "video"], "min_res": "600x335", 
                 "aspect": ["1:1", "16:9"], "video_cap": "≤2m20s"},
            "Facebook": {"allowed": ["single_image", "carousel", "video"], "max_carousel": 10, 
                       "min_res": "1200x630", "aspect": ["1:1", "16:9"], "video_cap": "≤240s"},
            "YouTube": {"allowed": ["video"], "min_res": "1920x1080", 
                      "aspect": ["16:9"], "video_cap": "≤15m"},
            "Pinterest": {"allowed": ["single_image", "carousel"], "max_carousel": 5, 
                        "min_res": "1000x1500", "aspect": ["2:3", "1:1"], "video_cap": "≤15s"},
            "Threads": {"allowed": ["single_image", "carousel", "video"], "max_carousel": 10, 
                      "min_res": "1080x1080", "aspect": ["1:1", "4:5", "9:16"], "video_cap": "≤5m"},
            "Reddit": {"allowed": ["single_image", "video"], "min_res": "1200x1200", 
                     "aspect": ["1:1", "16:9"], "video_cap": "≤15m"},
            "Quora": {"allowed": ["single_image"], "min_res": "1200x1200", 
                    "aspect": ["1:1", "16:9"], "video_cap": "≤2m"},
            "Glassdoor": {"allowed": ["single_image"], "min_res": "1200x1200", 
                        "aspect": ["1:1", "16:9"], "video_cap": "≤2m"},
            "Indeed": {"allowed": ["single_image"], "min_res": "1200x1200", 
                     "aspect": ["1:1", "16:9"], "video_cap": "≤2m"}
        }
        
        # Try to find custom media policy
        for sheet_name, df in self.sheets.items():
            if 'media' in sheet_name.lower() and 'policy' in sheet_name.lower():
                # Process media policy data
                for platform in self.platforms:
                    if platform in default_policies:
                        media_policy[platform] = default_policies[platform].copy()
                        
        # Use defaults if no custom policy found
        if not media_policy:
            media_policy = default_policies
            
        return media_policy
        
    def extract_caption_rules(self) -> Dict[str, Dict[str, Any]]:
        """Extract caption rules for all platforms"""
        caption_rules = {}
        
        # Default caption rules
        default_rules = {
            "Instagram": {"max_chars": 2200, "allow_emojis": True, "allow_mentions": True},
            "LinkedIn": {"max_chars": 3000, "allow_emojis": False, "allow_mentions": True},
            "TikTok": {"max_chars": 2200, "allow_emojis": True, "allow_mentions": True},
            "X": {"max_chars": 280, "allow_emojis": True, "allow_mentions": True},
            "Facebook": {"max_chars": 2200, "allow_emojis": True, "allow_mentions": True},
            "YouTube": {"max_chars": 5000, "allow_emojis": True, "allow_mentions": True},
            "Pinterest": {"max_chars": 500, "allow_emojis": True, "allow_mentions": True},
            "Threads": {"max_chars": 500, "allow_emojis": True, "allow_mentions": True},
            "Reddit": {"max_chars": 10000, "allow_emojis": True, "allow_mentions": True},
            "Quora": {"max_chars": 5000, "allow_emojis": True, "allow_mentions": True},
            "Glassdoor": {"max_chars": 3000, "allow_emojis": True, "allow_mentions": True},
            "Indeed": {"max_chars": 3000, "allow_emojis": True, "allow_mentions": True}
        }
        
        # Try to find custom caption rules
        for sheet_name, df in self.sheets.items():
            if 'caption' in sheet_name.lower() and 'rule' in sheet_name.lower():
                # Process caption rules data
                for platform in self.platforms:
                    if platform in default_rules:
                        caption_rules[platform] = default_rules[platform].copy()
                        
        # Use defaults if no custom rules found
        if not caption_rules:
            caption_rules = default_rules
            
        return caption_rules
        
    def extract_hashtag_banks(self, brand: str) -> Dict[str, List[str]]:
        """Extract hashtag banks for each platform"""
        hashtag_banks = {}
        
        # Look for hashtag data
        for sheet_name, df in self.sheets.items():
            if 'hash' in sheet_name.lower() or 'hashtag' in sheet_name.lower():
                # Try to find brand-specific hashtags
                for platform in self.platforms:
                    hashtag_banks[platform] = []
                    
                    # Look for platform column
                    platform_col = None
                    for col in df.columns:
                        if platform.lower() in col.lower():
                            platform_col = col
                            break
                            
                    if platform_col:
                        # Look for brand row
                        for idx, row in df.iterrows():
                            if isinstance(idx, str) and brand.lower() in idx.lower():
                                hashtags = row.get(platform_col)
                                if pd.notna(hashtags) and isinstance(hashtags, str):
                                    # Split hashtags and clean them
                                    tags = [tag.strip() for tag in str(hashtags).split(',') if tag.strip()]
                                    hashtag_banks[platform] = tags
                                break
                                
        # Add default hashtags if none found
        for platform in self.platforms:
            if platform not in hashtag_banks or not hashtag_banks[platform]:
                hashtag_banks[platform] = [f"#{brand}Marketplace", f"#{brand}Tech"]
                
        return hashtag_banks
        
    def extract_cta_banks(self, brand: str) -> Dict[str, List[str]]:
        """Extract CTA banks for each platform"""
        cta_banks = {}
        
        # Look for CTA data
        for sheet_name, df in self.sheets.items():
            if 'cta' in sheet_name.lower() or 'call' in sheet_name.lower():
                for platform in self.platforms:
                    cta_banks[platform] = []
                    
                    # Look for platform column
                    platform_col = None
                    for col in df.columns:
                        if platform.lower() in col.lower():
                            platform_col = col
                            break
                            
                    if platform_col:
                        # Look for brand row
                        for idx, row in df.iterrows():
                            if isinstance(idx, str) and brand.lower() in idx.lower():
                                ctas = row.get(platform_col)
                                if pd.notna(ctas) and isinstance(ctas, str):
                                    # Split CTAs and clean them
                                    tags = [cta.strip() for cta in str(ctas).split(',') if cta.strip()]
                                    cta_banks[platform] = tags
                                break
                                
        # Add default CTAs if none found
        for platform in self.platforms:
            if platform not in cta_banks or not cta_banks[platform]:
                cta_banks[platform] = ["Learn more", "Get started", "Contact us"]
                
        return cta_banks
        
    def extract_forbidden_words(self) -> List[str]:
        """Extract forbidden words"""
        forbidden_words = ["cheap", "guaranteed results", "best price guaranteed", 
                          "no questions asked", "100% risk-free", "miracle", 
                          "unlimited for free", "click here", "hurry before it's gone"]
        
        # Look for forbidden words data
        for sheet_name, df in self.sheets.items():
            if 'forbidden' in sheet_name.lower() or 'words' in sheet_name.lower():
                for col in df.columns:
                    if 'word' in col.lower() or 'forbidden' in col.lower():
                        words = df[col].dropna().tolist()
                        forbidden_words.extend([str(w) for w in words if isinstance(w, str)])
                        break
                        
        return list(set(forbidden_words))  # Remove duplicates
        
    def extract_required_disclosures(self, brand: str) -> List[str]:
        """Extract required disclosures for this brand"""
        disclosures = ["Include warranty/return policy when making promises"]
        
        # Look for disclosure data
        for sheet_name, df in self.sheets.items():
            if 'disclosure' in sheet_name.lower() or 'required' in sheet_name.lower():
                for idx, row in df.iterrows():
                    if isinstance(idx, str) and brand.lower() in idx.lower():
                        for col in df.columns:
                            if 'disclosure' in col.lower():
                                disclosure = row.get(col)
                                if pd.notna(disclosure) and isinstance(disclosure, str):
                                    disclosures.append(str(disclosure))
                        break
                        
        return disclosures
        
    def extract_link_policy(self, brand: str) -> Dict[str, Any]:
        """Extract link policy"""
        link_policy = {
            "linkedin_include_link": True,
            "instagram_link_in_bio": True,
            "use_shortener": True,
            "shortener_domain": "bit.ly",
            "allowed_domains": [f"{brand.lower()}.co.uk"],
            "utm_template": "utm_source={platform}&utm_medium=social&utm_campaign={brand}_{week}"
        }
        
        # Look for link policy data
        for sheet_name, df in self.sheets.items():
            if 'link' in sheet_name.lower() and 'policy' in sheet_name.lower():
                for idx, row in df.iterrows():
                    if isinstance(idx, str) and brand.lower() in idx.lower():
                        if 'shortener_domain' in df.columns:
                            link_policy['shortener_domain'] = str(row.get('shortener_domain', 'bit.ly'))
                        if 'allowed_domains' in df.columns:
                            domains = str(row.get('allowed_domains', f"{brand.lower()}.co.uk"))
                            link_policy['allowed_domains'] = [d.strip() for d in domains.split(',')]
                        break
                        
        return link_policy
        
    def extract_proof_manifest(self, brand: str) -> Dict[str, str]:
        """Extract proof manifest settings"""
        proof_manifest = {
            "root": f"/Codex/Ops/Content/GPT/Proofs/{brand}/",
            "week_format": "W%V",
            "timezone": "Europe/London",
            "example": f"/Codex/Ops/Content/GPT/Proofs/{brand}/W41.hash"
        }
        
        # Look for proof manifest data
        for sheet_name, df in self.sheets.items():
            if 'proof' in sheet_name.lower() and 'manifest' in sheet_name.lower():
                for idx, row in df.iterrows():
                    if isinstance(idx, str) and brand.lower() in idx.lower():
                        if 'root' in df.columns:
                            proof_manifest['root'] = str(row.get('root', proof_manifest['root']))
                        if 'timezone' in df.columns:
                            proof_manifest['timezone'] = str(row.get('timezone', 'Europe/London'))
                        break
                        
        return proof_manifest
        
    def create_brand_config(self, brand: str) -> Dict[str, Any]:
        """Create complete brand configuration"""
        print(f"Creating config for brand: {brand}")
        
        config = {
            "brand": brand,
            "voice": self.extract_brand_voice(brand),
            "story": self.extract_brand_story(brand),
            "platforms": self.extract_platform_enabled(brand),
            "cadence": self.extract_cadence(brand),
            "media_policy": self.extract_media_policy(),
            "caption_rules": self.extract_caption_rules(),
            "hashtag_bank": self.extract_hashtag_banks(brand),
            "cta_bank": self.extract_cta_banks(brand),
            "forbidden_words": self.extract_forbidden_words(),
            "required_disclosures": self.extract_required_disclosures(brand),
            "link_policy": self.extract_link_policy(brand),
            "proof_manifest": self.extract_proof_manifest(brand)
        }
        
        return config
        
    def save_brand_config(self, brand: str, config: Dict[str, Any]):
        """Save brand configuration to JSON file"""
        filename = f"{brand.lower().replace(' ', '')}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        print(f"✓ Saved {brand} config to {filepath}")
        
    def create_multibrand_config(self, all_configs: Dict[str, Dict[str, Any]]):
        """Create a combined multi-brand configuration file"""
        multibrand_file = os.path.join(self.output_dir, "multibrand.json")
        
        with open(multibrand_file, 'w', encoding='utf-8') as f:
            json.dump(all_configs, f, indent=2, ensure_ascii=False)
            
        print(f"✓ Saved multi-brand config to {multibrand_file}")
        
    def convert(self):
        """Main conversion process"""
        print("Starting Excel to Brand JSON conversion...")
        
        # Load Excel data
        self.load_excel_data()
        
        # Extract brands and platforms
        self.extract_brands_and_platforms()
        
        # Create configs for each brand
        all_configs = {}
        for brand in self.brands:
            try:
                config = self.create_brand_config(brand)
                self.save_brand_config(brand, config)
                all_configs[brand] = config
            except Exception as e:
                print(f"⚠ Error creating config for {brand}: {e}")
                
        # Create multi-brand config
        if all_configs:
            self.create_multibrand_config(all_configs)
            
        print(f"\n✓ Conversion complete! Created {len(all_configs)} brand configs in {self.output_dir}/")
        print(f"Brands processed: {list(all_configs.keys())}")

def main():
    parser = argparse.ArgumentParser(description='Convert Excel/Google Sheets to Brand JSON configs')
    parser.add_argument('--sheet', help='Path to Excel file (auto-detected if not provided)')
    parser.add_argument('--out', default='config', help='Output directory (default: config)')
    
    args = parser.parse_args()
    
    # Handle filename with special characters or auto-detect
    if not args.sheet:
        # Auto-detect Excel files in current directory
        import glob
        excel_files = glob.glob("*.xlsx")
        if excel_files:
            args.sheet = excel_files[0]
            print(f"Auto-detected Excel file: {args.sheet}")
        else:
            print("Error: No Excel files found in current directory")
            return
    elif not os.path.exists(args.sheet):
        # Try to find Excel files in current directory
        import glob
        excel_files = glob.glob("*.xlsx")
        if excel_files:
            args.sheet = excel_files[0]
            print(f"Using Excel file: {args.sheet}")
        else:
            print(f"Error: Excel file not found: {args.sheet}")
            return
        
    converter = BrandConfigConverter(args.sheet, args.out)
    converter.convert()

if __name__ == "__main__":
    main()
