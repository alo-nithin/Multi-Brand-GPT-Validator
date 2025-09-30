# Multi-Brand GPT Validator - Deployment Guide

## 🎉 Your Multi-Brand GPT Validator is Ready!

### ✅ **What's Complete:**
- ✅ Brand JSON configurations generated from your Excel file
- ✅ FastAPI validator application (`app.py`)
- ✅ Validation logic (`validator.py`)
- ✅ All dependencies installed
- ✅ Local testing successful

### 📁 **Current File Structure:**
```
customgpt/
├── config/
│   ├── amar.json
│   ├── alogroup.json
│   ├── buyitback.json
│   ├── cilkroad.json
│   ├── pax.json
│   ├── silkroad.json
│   ├── techcycle.json
│   └── multibrand.json
├── app.py
├── validator.py
├── requirements.txt
├── sheet_to_brand_json.py
└── CONVERSION_SUMMARY.md
```

## 🚀 **Deployment Options**

### Option 1: Render (Recommended)

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Multi-Brand GPT Validator"
   git branch -M main
   git remote add origin https://github.com/yourusername/multibrand-gpt.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Runtime:** Python 3.11
     - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port 10000`
     - **Environment Variables:**
       - `VALIDATOR_TOKEN` = `your-secure-token-here`

3. **Your API will be live at:** `https://your-app-name.onrender.com`

### Option 2: Railway

1. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Configure:
     - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
     - **Environment Variables:**
       - `VALIDATOR_TOKEN` = `your-secure-token-here`

### Option 3: Fly.io

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Deploy:**
   ```bash
   fly launch
   fly secrets set VALIDATOR_TOKEN=your-secure-token-here
   fly deploy
   ```

## 🔧 **API Endpoints**

### Health Check
```
GET /health
```
Returns: `{"ok": true}`

### Validate Post
```
POST /validate
Authorization: Bearer your-token
Content-Type: application/json

{
  "brand": "Amar",
  "platform": "Instagram", 
  "caption": "Your post content here",
  "hashtags": ["#AmarMarketplace"],
  "cta": "Learn more",
  "media_suggestion": {
    "type": "single_image",
    "count": 1
  },
  "links": [{
    "url": "https://amar.co.uk/your-link",
    "utm": true
  }],
  "week": "W41",
  "post_id": "amar_ig_W41_001"
}
```

**Success Response:**
```json
{
  "valid": true,
  "sha256": "abc123...",
  "proof_file": "/Codex/Ops/Content/GPT/Proofs/Amar/W41.hash",
  "normalized_bundle": { ... }
}
```

**Error Response:**
```json
{
  "valid": false,
  "errors": ["CAPTION_TOO_LONG:2500>2200"],
  "suggestions": {}
}
```

### Get Brand Configuration
```
GET /banks/{brand}
Authorization: Bearer your-token
```

## 🤖 **Custom GPT Integration**

### 1. Create Custom GPT
- Go to ChatGPT → Create a GPT
- Name: "ALO Group Multi-Brand Content Copilot"

### 2. System Instructions
```
You are ALO Group's Multi-Brand Content Copilot.

Always write in the selected brand's tone & style, respect media/caption/link rules, required disclosures, forbidden words, and cadence.

Before final output, call the Validator API. If invalid, fix and retry once.

If a preset is missing, reply: "Preset not found — please update the bank and try again."

Ask the user (if missing): Brand, Platform, Content Type, Goal, Audience, Pillar, CTA, Week (Wxx), Link, Language.
```

### 3. Add Action
- **Name:** ValidatePost
- **HTTP Method:** POST
- **URL:** `https://your-app.onrender.com/validate`
- **Auth Header:** `Authorization: Bearer {{VALIDATOR_TOKEN}}`
- **Request Schema:**
```json
{
  "brand": "Amar",
  "platform": "Instagram",
  "caption": "string",
  "hashtags": ["#..."],
  "cta": "string", 
  "media_suggestion": {
    "type": "carousel",
    "count": 3,
    "notes": "..."
  },
  "links": [{
    "url": "https://amar.co.uk/...",
    "utm": true
  }],
  "week": "W41",
  "post_id": "amar_ig_W41_001"
}
```

### 4. Create Secret
- In GPT Builder, create a secret named `VALIDATOR_TOKEN`
- Set value to your secure token

## 🧪 **Testing Your Deployment**

### Test Health Endpoint
```bash
curl https://your-app.onrender.com/health
```

### Test Validation
```bash
curl -X POST https://your-app.onrender.com/validate \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Amar",
    "platform": "Instagram",
    "caption": "Test post",
    "hashtags": ["#AmarMarketplace"],
    "media_suggestion": {"type": "single_image", "count": 1},
    "links": [{"url": "https://amar.co.uk/test", "utm": true}],
    "week": "W41",
    "post_id": "test_001"
  }'
```

## 🔒 **Security Notes**

1. **Change the default token:** Replace `change-me` with a secure random token
2. **Use HTTPS:** All deployments provide HTTPS by default
3. **Environment variables:** Never commit tokens to your repository
4. **Rate limiting:** Consider adding rate limiting for production use

## 📊 **Monitoring & Maintenance**

### Logs
- **Render:** Available in dashboard
- **Railway:** Available in dashboard  
- **Fly.io:** `fly logs`

### Updates
1. Update brand configs in `config/` folder
2. Commit changes to GitHub
3. Redeploy automatically (if auto-deploy enabled)

## 🆘 **Troubleshooting**

### Common Issues:

1. **401/403 Errors:** Check your `VALIDATOR_TOKEN` matches
2. **PLATFORM_NOT_ENABLED:** Brand doesn't have that platform enabled
3. **CAPTION_TOO_LONG:** Shorten the caption
4. **HASHTAG_NOT_ALLOWED:** Use hashtags from the brand's bank
5. **LINK_DOMAIN_NOT_ALLOWED:** Use allowed domains from brand config

### Debug Mode:
Add this to your environment variables for detailed logging:
```
DEBUG=true
```

## 🎯 **Next Steps**

1. **Deploy** using one of the options above
2. **Test** your API endpoints
3. **Create** your Custom GPT with the validator action
4. **Train** your team on using the system
5. **Monitor** usage and performance

Your Multi-Brand GPT Validator is ready for production! 🚀
