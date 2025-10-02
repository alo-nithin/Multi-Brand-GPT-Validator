# 🚀 Multi-Brand GPT Validator - Complete Documentation

## 📋 **Table of Contents**
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Technical Stack](#technical-stack)
5. [Setup & Installation](#setup--installation)
6. [Google Sheets Integration](#google-sheets-integration)
7. [API Endpoints](#api-endpoints)
8. [Custom GPT Integration](#custom-gpt-integration)
9. [Deployment](#deployment)
10. [Usage Examples](#usage-examples)
11. [Troubleshooting](#troubleshooting)
12. [Future Enhancements](#future-enhancements)

---

## 🎯 **Overview**

The Multi-Brand GPT Validator is a comprehensive content validation system that ensures social media content complies with brand-specific guidelines, policies, and best practices. It integrates with Google Sheets for dynamic configuration management and provides a Custom GPT interface for seamless content creation and validation.

### **Key Benefits:**
- ✅ **Dynamic Configuration**: Real-time updates via Google Sheets
- ✅ **Multi-Brand Support**: Handle multiple brands with different policies
- ✅ **Content Validation**: Ensure compliance with brand guidelines
- ✅ **Custom GPT Integration**: Seamless ChatGPT integration
- ✅ **Proof Generation**: SHA256 hashing for content verification
- ✅ **Scalable Architecture**: FastAPI-based REST API

---

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Custom GPT    │────│  FastAPI Server  │────│  Google Sheets  │
│   (ChatGPT)     │    │   (Render.com)    │    │   (Dynamic)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Queries  │    │  Validation Logic │    │  Brand Configs   │
│   Content       │    │  Proof Generation │    │  Policies        │
│   Requests      │    │  Error Handling   │    │  Guidelines     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **Component Overview:**

1. **Custom GPT Interface**: ChatGPT integration for user interaction
2. **FastAPI Server**: REST API for validation and brand management
3. **Google Sheets**: Dynamic configuration storage
4. **Local Fallback**: JSON files for offline operation
5. **Proof System**: SHA256 hashing for content verification

---

## ✨ **Features**

### **Core Features:**
- 🎯 **Multi-Brand Support**: Handle multiple brands simultaneously
- 📊 **Dynamic Configuration**: Real-time updates via Google Sheets
- ✅ **Content Validation**: Comprehensive rule checking
- 🔐 **Proof Generation**: SHA256 hashing for compliance
- 🤖 **Custom GPT Integration**: Seamless ChatGPT experience
- 📱 **Platform-Specific Rules**: Different rules per social platform
- 🚫 **Forbidden Word Detection**: Automatic content filtering
- 📝 **Caption Rule Validation**: Length, emoji, mention limits
- 🖼️ **Media Policy Enforcement**: Image, video, carousel rules
- 🔗 **Link Policy Management**: Domain whitelisting
- 📢 **CTA Bank Management**: Approved call-to-actions
- 🏷️ **Hashtag Bank Management**: Approved hashtags

### **Advanced Features:**
- 🔄 **Fallback System**: Google Sheets → Local JSON
- 🌐 **UTM Parameter Support**: Automatic campaign tracking
- 📅 **Week-based Organization**: Content scheduling
- 🔍 **Error Handling**: Graceful failure management
- 📊 **Brand Comparison**: Multi-brand analysis
- 🎨 **Voice Consistency**: Brand tone enforcement

---

## 🛠️ **Technical Stack**

### **Backend:**
- **Python 3.10+**: Core programming language
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server for production
- **Pydantic**: Data validation and settings management
- **Pandas**: Data manipulation and analysis
- **Google Sheets API**: Dynamic configuration management

### **Dependencies:**
```txt
fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.8.2
python-dateutil==2.9.0.post0
pytz==2024.1
pandas
openpyxl
google-api-python-client==2.108.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
python-dotenv==1.0.0
```

### **Infrastructure:**
- **Render.com**: Cloud hosting platform
- **GitHub**: Version control and deployment
- **Google Cloud Console**: Service account management
- **Google Sheets**: Configuration storage

---

## 🚀 **Setup & Installation**

### **Prerequisites:**
- Python 3.10+
- Git
- Google Cloud Console account
- Render.com account
- ChatGPT Plus (for Custom GPT)

### **Local Development Setup:**

1. **Clone Repository:**
```bash
git clone https://github.com/alo-nithin/Multi-Brand-GPT-Validator.git
cd Multi-Brand-GPT-Validator
```

2. **Create Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment Variables:**
```bash
cp env.example .env
# Edit .env with your values
```

5. **Run Locally:**
```bash
python -m uvicorn app:app --reload
```

---

## 📊 **Google Sheets Integration**

### **Setup Process:**

1. **Google Cloud Console Setup:**
   - Create a new project
   - Enable Google Sheets API
   - Create a service account
   - Download service account JSON key

2. **Google Sheets Setup:**
   - Create a new spreadsheet
   - Share with service account email
   - Set up brand tabs with proper structure

3. **Data Structure:**
```
| Brand | Category | Platform | Key | Value | Description | Required |
|-------|----------|----------|-----|-------|-------------|----------|
| Amar | Voice | | tone | Professional... | Brand tone | Yes |
| Amar | Platforms | | Instagram | TRUE | Enable Instagram | Yes |
| Amar | Hashtag Bank | Instagram | | #AmarMarketplace | Primary hashtag | Yes |
```

### **Supported Categories:**
- **Voice**: Brand tone and style
- **Story**: Brand description
- **Platforms**: Enabled social platforms
- **Hashtag Bank**: Approved hashtags per platform
- **CTA Bank**: Approved call-to-actions per platform
- **Media Policy**: Media type rules per platform
- **Caption Rules**: Caption length and format rules
- **Forbidden Words**: Words to avoid
- **Link Policy**: Allowed domains
- **Required Disclosures**: Mandatory disclosures
- **Posting Frequency**: Posts per week per platform

---

## 🔌 **API Endpoints**

### **Base URL:** `https://multi-brand-gpt-validator.onrender.com`

### **Authentication:**
- **Type**: Bearer Token
- **Token**: `H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0`

### **Endpoints:**

#### **1. Health Check**
```http
GET /health
```
**Response:**
```json
{"ok": true}
```

#### **2. Get All Brands**
```http
GET /brands
```
**Response:**
```json
{
  "brands": [
    {
      "name": "Amar",
      "voice": {"tone": "Professional..."},
      "platforms": ["Instagram", "LinkedIn"],
      "hashtag_banks": {...},
      "cta_banks": {...}
    }
  ],
  "source": "google_sheets"
}
```

#### **3. Get Brand Info**
```http
GET /brands/{brand}
```
**Response:**
```json
{
  "brand": "Amar",
  "voice": {"tone": "Professional, engaging, customer-focused."},
  "story": "Amar is committed to delivering exceptional value...",
  "platforms": ["Instagram", "LinkedIn", "TikTok", "X"],
  "hashtag_banks": {
    "Instagram": ["#AmarMarketplace", "#AmarTech"]
  },
  "cta_banks": {
    "Instagram": ["Learn more", "Get started", "Contact us"]
  },
  "media_policy": {
    "Instagram": {
      "allowed": ["single_image", "carousel", "reel"],
      "max_carousel": 10,
      "min_res": "1080x1080"
    }
  }
}
```

#### **4. Validate Content**
```http
POST /validate
```
**Request Body:**
```json
{
  "brand": "Amar",
  "platform": "Instagram",
  "caption": "Check out our latest refurbished phones!",
  "hashtags": ["#AmarMarketplace", "#RefurbishedPhones"],
  "cta": "Shop now",
  "media_suggestion": {
    "type": "single_image",
    "notes": "High-quality product photo"
  },
  "week": "W41",
  "post_id": "amar_ig_W41_001"
}
```
**Response:**
```json
{
  "valid": true,
  "errors": [],
  "sha256": "3a8470d5a07cd6be7b05...",
  "proof_file": "/proofs/Amar/W41.hash"
}
```

#### **5. Get Brand Banks**
```http
GET /banks/{brand}
```
**Response:**
```json
{
  "brand": "Amar",
  "keys": ["brand", "voice", "story", "platforms", "hashtag_bank", "cta_bank"]
}
```

---

## 🤖 **Custom GPT Integration**

### **Setup Process:**

1. **Create Custom GPT:**
   - Go to ChatGPT → Explore GPTs → Create a GPT
   - Name: "ALO Group Content Copilot"

2. **Configure Actions:**
   - Click "Actions" → Create new action
   - Import OpenAPI schema from `custom_gpt_openapi_schema.json`
   - Set authentication: Bearer Token
   - Token: `H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0`

3. **Add Instructions:**
   - Copy instructions from `custom_gpt_instructions.md`
   - Paste into Instructions field

### **Custom GPT Capabilities:**

#### **Content Creation:**
- Create brand-compliant social media content
- Use approved hashtags and CTAs
- Validate content before presentation
- Generate proof hashes

#### **Brand Information:**
- Retrieve brand voice and story
- Show platform-specific policies
- Display approved content banks
- Compare brand guidelines

#### **Content Validation:**
- Check content against brand rules
- Identify compliance issues
- Suggest corrections
- Generate validation reports

### **Example Interactions:**

**User:** "Create an Instagram post for Amar brand about refurbished phones"

**Custom GPT Response:**
1. Calls `getBrandInfo` API for Amar
2. Retrieves Amar's voice, hashtag bank, CTA bank
3. Creates content in Amar's professional tone
4. Uses approved hashtags: #AmarMarketplace, #RefurbishedPhones
5. Uses approved CTA: "Shop now"
6. Calls `validateContent` API
7. Returns validated content with SHA256 proof

---

## 🚀 **Deployment**

### **Render.com Deployment:**

1. **Connect GitHub Repository:**
   - Link GitHub account to Render
   - Select repository: `alo-nithin/Multi-Brand-GPT-Validator`

2. **Configure Service:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: 3.10+

3. **Environment Variables:**
```bash
VALIDATOR_TOKEN=H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0
GOOGLE_SHEET_ID=1iSM9Iskxuu0zUjCGcX6azicsP2yNO75-X1QsXAFY7Xw
GOOGLE_CREDENTIALS_PATH=/opt/render/project/src/google-credentials.json
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
```

4. **Secret Files:**
   - Upload `google-credentials.json` as secret file

### **Deployment URL:**
`https://multi-brand-gpt-validator.onrender.com`

---

## 📝 **Usage Examples**

### **1. Brand Information Query**
```bash
curl -X GET "https://multi-brand-gpt-validator.onrender.com/brands/Amar" \
  -H "Authorization: Bearer H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0"
```

### **2. Content Validation**
```bash
curl -X POST "https://multi-brand-gpt-validator.onrender.com/validate" \
  -H "Authorization: Bearer H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Amar",
    "platform": "Instagram",
    "caption": "Check out our latest refurbished phones!",
    "hashtags": ["#AmarMarketplace"],
    "cta": "Shop now",
    "media_suggestion": {"type": "single_image"},
    "week": "W41",
    "post_id": "test_001"
  }'
```

### **3. Custom GPT Prompts**
- "Tell me about Amar brand's social media policies"
- "Create an Instagram post for Amar about refurbished phones"
- "Validate this content for Amar brand: 'Check out our phones! #AmarMarketplace'"
- "Compare the social media policies between Amar and Silkroad"

---

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **1. API Connection Errors**
**Problem:** Custom GPT can't connect to API
**Solution:**
- Check authentication token
- Verify API URL is correct
- Ensure Render service is running

#### **2. Google Sheets Errors**
**Problem:** "No data found for brand variations"
**Solution:**
- Check Google Sheet structure
- Verify service account permissions
- Ensure brand data exists in correct format

#### **3. Validation Errors**
**Problem:** Content validation failing
**Solution:**
- Check brand configuration
- Verify platform is enabled
- Review media policy rules

#### **4. Custom GPT Not Calling API**
**Problem:** GPT searches documents instead of calling API
**Solution:**
- Reconfigure Actions in Custom GPT
- Verify OpenAPI schema is correct
- Check authentication setup

### **Debug Commands:**

```bash
# Test API health
curl https://multi-brand-gpt-validator.onrender.com/health

# Test brand info
curl -H "Authorization: Bearer H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0" \
  https://multi-brand-gpt-validator.onrender.com/brands/Amar

# Test validation
curl -X POST -H "Authorization: Bearer H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0" \
  -H "Content-Type: application/json" \
  -d '{"brand":"Amar","platform":"Instagram","caption":"Test","media_suggestion":{"type":"single_image"}}' \
  https://multi-brand-gpt-validator.onrender.com/validate
```

---

## 🔮 **Future Enhancements**

### **Planned Features:**
- 📊 **Analytics Dashboard**: Content performance tracking
- 🔄 **Content Scheduling**: Automated posting
- 📱 **Mobile App**: Native mobile interface
- 🤖 **AI Content Generation**: Advanced content creation
- 📈 **Performance Metrics**: Engagement tracking
- 🔔 **Notification System**: Real-time alerts
- 📋 **Content Calendar**: Visual scheduling
- 🎨 **Template Library**: Pre-designed content templates
- 📊 **A/B Testing**: Content optimization
- 🔍 **Advanced Analytics**: Detailed reporting

### **Technical Improvements:**
- 🚀 **Caching**: Redis integration for performance
- 🔒 **Enhanced Security**: OAuth2, rate limiting
- 📊 **Monitoring**: Application performance monitoring
- 🧪 **Testing**: Comprehensive test suite
- 📚 **Documentation**: API documentation with Swagger
- 🔄 **CI/CD**: Automated deployment pipeline

---

## 📞 **Support & Contact**

### **Technical Support:**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Comprehensive guides and examples
- **API Reference**: Detailed endpoint documentation

### **Brand Management:**
- **Google Sheets**: Update brand configurations
- **Custom GPT**: Interactive content creation
- **API Integration**: Direct API access

---

## 🎉 **Conclusion**

The Multi-Brand GPT Validator is a comprehensive solution for managing multi-brand social media content with dynamic configuration, real-time validation, and seamless Custom GPT integration. It provides a robust foundation for content compliance, brand consistency, and scalable content management.

**Key Achievements:**
- ✅ **Dynamic Configuration**: Real-time updates via Google Sheets
- ✅ **Multi-Brand Support**: Handle multiple brands simultaneously
- ✅ **Custom GPT Integration**: Seamless ChatGPT experience
- ✅ **Content Validation**: Comprehensive rule checking
- ✅ **Proof Generation**: SHA256 hashing for compliance
- ✅ **Scalable Architecture**: Production-ready deployment

**Ready for Production Use!** 🚀
