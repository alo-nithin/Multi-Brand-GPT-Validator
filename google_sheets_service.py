"""
Google Sheets Service for Dynamic Brand Configuration
"""
import os
import json
from typing import Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GoogleSheetsService:
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Sheets service
        
        Args:
            credentials_path: Path to service account JSON file
        """
        self.credentials_path = credentials_path or os.getenv('GOOGLE_CREDENTIALS_PATH')
        self.spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')
        
        if self.credentials_path and self.spreadsheet_id:
            self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Sheets API service"""
        try:
            # Try to get credentials from environment variable first
            credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
            
            if credentials_json:
                # Use credentials from environment variable
                import json
                credentials_info = json.loads(credentials_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
                )
                print(f"✅ Google Sheets service initialized from environment variable")
            elif self.credentials_path and os.path.exists(self.credentials_path):
                # Fallback to file
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
                )
                print(f"✅ Google Sheets service initialized from file")
            else:
                raise Exception("No credentials found in environment or file")
            
            self.service = build('sheets', 'v4', credentials=credentials)
            
        except Exception as e:
            print(f"❌ Failed to initialize Google Sheets service: {e}")
            self.service = None
    
    def get_sheet_data(self, sheet_name: str, range_name: str = None) -> List[List]:
        """
        Get data from a specific sheet
        
        Args:
            sheet_name: Name of the sheet tab
            range_name: Specific range (e.g., 'A1:Z100')
        
        Returns:
            List of rows from the sheet
        """
        if not self.service:
            raise Exception("Google Sheets service not initialized")
        
        try:
            if range_name:
                range_str = f"{sheet_name}!{range_name}"
            else:
                range_str = sheet_name
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_str
            ).execute()
            
            return result.get('values', [])
        except HttpError as e:
            print(f"❌ Error reading sheet {sheet_name}: {e}")
            raise
    
    def get_brand_config(self, brand_name: str) -> Dict:
        """
        Get brand configuration from Google Sheets
        
        Args:
            brand_name: Name of the brand (sheet tab name)
        
        Returns:
            Brand configuration dictionary
        """
        try:
            # Get all data from the brand sheet
            data = self.get_sheet_data(brand_name)
            
            if not data:
                raise Exception(f"No data found for brand: {brand_name}")
            
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(data[1:], columns=data[0])  # Skip header row
            
            # Convert to brand configuration format
            config = self._dataframe_to_config(df, brand_name)
            return config
            
        except Exception as e:
            print(f"❌ Error getting config for {brand_name}: {e}")
            raise
    
    def _dataframe_to_config(self, df: pd.DataFrame, brand_name: str) -> Dict:
        """
        Convert DataFrame to brand configuration format
        
        Args:
            df: DataFrame with brand data
            brand_name: Name of the brand
        
        Returns:
            Brand configuration dictionary
        """
        config = {
            "brand": brand_name,
            "voice": {},
            "story": "",
            "platforms": [],
            "hashtag_bank": {},
            "cta_bank": {},
            "media_policy": {},
            "forbidden_words": [],
            "link_policy": {"allowed_domains": []},
            "required_disclosures": [],
            "proof_manifest": {
                "timezone": "UTC",
                "root": "/proofs"
            }
        }
        
        # Process each row
        for _, row in df.iterrows():
            category = row.get('Category', '').strip()
            platform = row.get('Platform', '').strip()
            key = row.get('Key', '').strip()
            value = row.get('Value', '').strip()
            
            if not category or not key:
                continue
            
            # Process different categories
            if category == 'Voice':
                config['voice'][key.lower()] = value
            elif category == 'Story':
                config['story'] = value
            elif category == 'Platforms':
                if value.lower() == 'true':
                    config['platforms'].append(key)
            elif category == 'Hashtag Bank':
                if platform not in config['hashtag_bank']:
                    config['hashtag_bank'][platform] = []
                config['hashtag_bank'][platform].append(value)
            elif category == 'CTA Bank':
                if platform not in config['cta_bank']:
                    config['cta_bank'][platform] = []
                config['cta_bank'][platform].append(value)
            elif category == 'Media Policy':
                if platform not in config['media_policy']:
                    config['media_policy'][platform] = {}
                config['media_policy'][platform][key] = value
            elif category == 'Forbidden Words':
                config['forbidden_words'].append(value)
            elif category == 'Link Policy':
                if key == 'allowed_domains':
                    config['link_policy']['allowed_domains'].append(value)
            elif category == 'Required Disclosures':
                config['required_disclosures'].append(value)
        
        return config
    
    def get_all_brands(self) -> List[str]:
        """
        Get list of all available brand sheets
        
        Returns:
            List of brand names
        """
        try:
            # Get spreadsheet metadata
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheets = spreadsheet.get('sheets', [])
            brand_names = []
            
            for sheet in sheets:
                sheet_name = sheet['properties']['title']
                # Skip system sheets
                if sheet_name.lower() not in ['instructions', 'template', 'readme']:
                    brand_names.append(sheet_name)
            
            return brand_names
            
        except Exception as e:
            print(f"❌ Error getting brand list: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if Google Sheets service is available"""
        return self.service is not None and self.spreadsheet_id is not None

# Global instance
sheets_service = GoogleSheetsService()
