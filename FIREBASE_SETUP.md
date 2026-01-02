# Firebase Phone Authentication Setup

## Error: auth/billing-not-enabled

You're seeing this error because **Phone Authentication requires Firebase Blaze (Pay-as-you-go) plan**.

## What This Means

Firebase's free Spark plan does NOT support phone authentication. You need to upgrade to the Blaze plan.

**Good news**: The Blaze plan is still free for low usage! You only pay if you exceed the free tier limits, which are generous for development and small apps.

## How to Fix

### Option 1: Upgrade to Blaze Plan (Recommended)

1. **Go to Firebase Console**: https://console.firebase.google.com/
2. **Select your project**: `community-app-bd35e`
3. Click the **gear icon** (⚙️) → **Usage and billing**
4. Click **"Modify plan"** or **"Upgrade project"**
5. Select **"Blaze (Pay as you go)"** plan
6. Add a payment method (required, but won't be charged unless you exceed free tier)
7. Confirm upgrade

### Blaze Plan Free Tier Includes:
- **Phone Auth**: First 10,000 verifications/month FREE
- Everything from Spark plan
- Only charges if you exceed free quotas

### After Upgrading:

1. **Enable Phone Authentication**:
   - Go to **Authentication** → **Sign-in method**
   - Click **Phone**
   - Toggle **Enable**
   - Click **Save**

2. **Add Authorized Domains** (if not done yet):
   - Go to **Authentication** → **Settings** → **Authorized domains**
   - Add `127.0.0.1`
   - Add `localhost`
   - Click **Save**

3. **Refresh your app** and try phone login again

---

## Option 2: Use Email Authentication Only (No Upgrade Needed)

If you don't want to upgrade to Blaze plan, you can disable phone authentication and use email-only:

1. In your app, users will only see the **Email** tab
2. Email authentication works on the free Spark plan
3. Remove or hide the Phone tab in the UI

---

## Cost Concerns?

Don't worry! For development and small apps:
- First 10K phone verifications/month = **FREE**
- Firebase sends you alerts before charging
- You can set spending limits

Most development projects stay within free tier limits.

---

## Summary

**To use phone authentication, you MUST upgrade to Blaze plan.**

It's free for low usage and required for SMS/phone features. This is a Firebase limitation, not an issue with the code.
