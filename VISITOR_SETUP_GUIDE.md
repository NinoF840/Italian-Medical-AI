# 🔧 Visitor Setup Guide - Medico-Italiano-IA

## Quick Start for Visitors

### ✅ **Recommended Setup Process**

1. **Download/Extract** the Medico-Italiano-IA folder
2. **Run Firewall Setup** (as Administrator)
3. **Launch the Application**
4. **Access via Browser**

---

## 🚨 **Step 1: Firewall Configuration (IMPORTANT)**

**Port 8501 must be accessible for the application to work properly.**

### Option A: Automated Setup (Recommended)

Right-click on **`Setup_Firewall.bat`** and select **"Run as administrator"**

This will automatically:
- ✅ Configure Windows Firewall for port 8501
- ✅ Create inbound/outbound rules for Medico-Italiano-IA
- ✅ Test port accessibility

### Option B: PowerShell Setup (Advanced Users)

Right-click on **`Setup_Firewall.ps1`** and select **"Run with PowerShell"** (as administrator)

### Option C: Manual Firewall Configuration

If automated setup fails, manually configure Windows Firewall:

1. **Open Windows Defender Firewall**
   - Press `Win + R`, type `wf.msc`, press Enter

2. **Create Inbound Rule**
   - Left panel: Click "Inbound Rules"
   - Right panel: Click "New Rule..."
   - Rule Type: "Program"
   - Program: Browse to `dist\Medico-Italiano-IA.exe`
   - Action: "Allow the connection"
   - Profile: Check all (Domain, Private, Public)
   - Name: "Medico-Italiano-IA Inbound"

3. **Create Outbound Rule**
   - Left panel: Click "Outbound Rules"
   - Repeat same process
   - Name: "Medico-Italiano-IA Outbound"

---

## 🚀 **Step 2: Launch Application**

### Method 1: Easy Launch (Recommended)
Double-click **`Run_Medico_IA.bat`**

### Method 2: Direct Launch
Navigate to `dist\` folder and double-click **`Medico-Italiano-IA.exe`**

### Method 3: Command Line
```cmd
cd "C:\path\to\Medico-Italiano-IA"
dist\Medico-Italiano-IA.exe
```

---

## 🌐 **Step 3: Access the Application**

Once launched, the application will be available at:
**http://localhost:8501**

- Application automatically opens your default browser
- If browser doesn't open, manually navigate to the URL above
- Wait 10-30 seconds for full initialization

---

## ⚠️ **Common Issues & Solutions**

### 🛡️ **Windows Defender Blocking**

**Issue:** "Windows protected your PC" message appears

**Solution:**
1. Click "More info"
2. Click "Run anyway"
3. Or add folder to Windows Defender exclusions:
   - Windows Security → Virus & threat protection
   - Manage settings under "Virus & threat protection settings"
   - Add exclusion → Folder → Select Medico-Italiano-IA folder

### 🔥 **Firewall/Port Issues**

**Issue:** Browser shows "This site can't be reached" or similar error

**Solutions:**
1. **Run firewall setup** (see Step 1 above)
2. **Check Windows Firewall:**
   - Ensure "Medico-Italiano-IA" rules exist
   - Temporarily disable firewall to test
3. **Check port usage:**
   ```cmd
   netstat -ano | findstr :8501
   ```
4. **Try alternative port:** Contact support for configuration

### 👮 **Admin Rights Required**

**Issue:** Application fails to start or shows permission errors

**Solutions:**
1. **Right-click** `Run_Medico_IA.bat` → "Run as administrator"
2. **Right-click** `Medico-Italiano-IA.exe` → "Run as administrator"
3. **Modify folder permissions:**
   - Right-click folder → Properties → Security
   - Edit permissions for your user account

### 💾 **Insufficient RAM/Performance**

**Issue:** Application runs slowly or crashes

**Solutions:**
1. **Check available RAM:** Task Manager → Performance → Memory
2. **Close other applications** to free up memory
3. **Minimum requirements:**
   - 8GB RAM recommended
   - 4GB available disk space
   - Windows 10/11 64-bit

### 🌐 **Browser Issues**

**Issue:** Web interface doesn't load properly

**Solutions:**
1. **Try different browsers:** Chrome, Firefox, Edge
2. **Clear browser cache** and cookies
3. **Disable browser extensions** temporarily
4. **Check browser console** for JavaScript errors (F12)

---

## 🔍 **Verification Steps**

### Check if Application is Running
```cmd
tasklist | findstr "Medico-Italiano-IA"
```

### Check if Port is Open
```cmd
netstat -ano | findstr :8501
```

### Test Port Connectivity
```powershell
Test-NetConnection -ComputerName localhost -Port 8501
```

---

## 📞 **Getting Help**

If you encounter issues not covered here:

### 🆘 **Immediate Support**
- **Email:** nino58150@gmail.com
- **Response Time:** < 4 hours
- **Include:** Error messages, screenshots, system specs

### 📋 **What to Include in Support Request**
1. **Error messages** (exact text)
2. **Screenshots** of any error dialogs
3. **System information:**
   - Windows version (Win + R → `winver`)
   - Available RAM (Task Manager → Performance)
   - Antivirus software installed
4. **Steps taken** before the error occurred

### 🔧 **Diagnostic Information**
Run this command and include output in support request:
```cmd
systeminfo | findstr /B /C:"OS Name" /C:"Total Physical Memory" /C:"Available Physical Memory"
```

---

## 💡 **Tips for Smooth Operation**

### 🎯 **Best Practices**
- **Close unnecessary applications** before launching
- **Use modern browsers** (Chrome, Firefox, Edge)
- **Ensure stable internet connection**
- **Don't close the console window** while using the app

### 🚀 **Performance Optimization**
- **Allocate 8GB+ RAM** for optimal performance
- **Close memory-intensive applications**
- **Use SSD storage** if available
- **Keep Windows updated**

### 🔒 **Security Considerations**
- Application runs **locally only** (localhost:8501)
- **No data leaves your computer** during demo
- **Firewall rules are application-specific**
- **Demo has built-in rate limiting** (10 requests/day)

---

## 📊 **Demo Limitations**

Remember this is a **demonstration version** with:
- ✅ **10 requests per day** per user
- ✅ **500 character limit** per request
- ✅ **Basic entity types** only
- ✅ **Watermarked results**

**Full version offers unlimited processing, custom entities, API access, and priority support.**

---

## 🎯 **Success Indicators**

✅ **Setup Complete When:**
- Application launches without errors
- Browser opens to http://localhost:8501
- Medico-Italiano-IA interface loads
- You can enter text and get NER results
- No firewall warnings appear

**Enjoy exploring Italian Medical AI capabilities!** 🏥🤖

---

*Need the full version? Contact nino58150@gmail.com for pricing and deployment options.*

