# 🔐 حل مشكلة 2FA على GitHub - الحل السريع

## ⚠️ المشكلة:
لا يمكنك استخدام كلمة المرور العادية مع Git عندما تكون 2FA مفعلة.

---

## ✅ الحل السريع (5 دقائق):

### الخطوة 1: إنشاء Personal Access Token (PAT)

1. اذهب إلى: https://github.com/settings/tokens
2. اضغط على **"Generate new token"** → **"Generate new token (classic)"**
3. أعطه اسم: `tsp-geoattention-token`
4. اختر المدة: **30 days** (أو أكثر)
5. اختر الصلاحيات:
   - ✅ `repo` (كل الخيارات تحتها)
   - ✅ `workflow`
   - ✅ `write:packages`
6. اضغط **"Generate token"**
7. **انسخ التوكن فوراً** (لن تراه مرة أخرى!)

---

## 🔧 الخطوة 2: استخدام التوكن مع Git

### الطريقة 1: استخدام التوكن مباشرة (الأسهل)

```bash
# عند الطلب من كلمة المرور، استخدم التوكن بدلاً من كلمة المرور:
# Username: baserah-ai
# Password: [الصق التوكن هنا]
```

### الطريقة 2: حفظ التوكن في Git Config (الأفضل)

```bash
# قم بتشغيل هذا الأمر:
git config --global credential.helper store

# ثم عند أول push، استخدم التوكن
# بعدها سيتم حفظه تلقائياً
```

### الطريقة 3: استخدام SSH (الأكثر أماناً)

```bash
# إذا كنت تريد طريقة أكثر أماناً:
# 1. أنشئ SSH key:
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. أضفه إلى GitHub:
# https://github.com/settings/keys

# 3. استخدم SSH بدلاً من HTTPS:
git remote set-url origin git@github.com:mubtakir/tsp-geoattention.git
```

---

## 🚀 الخطوات الكاملة لرفع المشروع:

### 1. إنشاء المستودع على GitHub

```bash
# اذهب إلى: https://github.com/new
# اسم المستودع: tsp-geoattention
# الوصف: TSP-GeoAttention - Hybrid Practical Approach
# اختر: Public
# اضغط: Create repository
```

### 2. رفع الملفات

```bash
cd /home/al-mubtakir/Documents/p_np

# إذا لم تكن قد أنشأت git repo بعد:
git init
git add .
git commit -m "Initial commit: TSP-GeoAttention - Hybrid Practical Approach"
git branch -M main
git remote add origin https://github.com/baserah-ai/tsp-geoattention.git

# عند الطلب:
# Username: mubtakir
# Password: [الصق التوكن هنا]

git push -u origin main
```

### 3. إذا كان لديك repo موجود بالفعل:

```bash
cd /home/al-mubtakir/Documents/p_np

# تحقق من الـ remote:
git remote -v

# إذا كان موجود:
git push origin main

# عند الطلب:
# Username: mubtakir
# Password: [الصق التوكن هنا]
```

---

## ⏰ ملاحظة مهمة:

**التوكن ينتهي بعد 30 يوم!**

عندما ينتهي:
1. اذهب إلى: https://github.com/settings/tokens
2. أنشئ توكن جديد
3. حدّث Git config

---

## 🔒 نصائح الأمان:

✅ **لا تشارك التوكن مع أحد**
✅ **لا تضعه في الملفات العامة**
✅ **استخدم SSH للأمان الأفضل**
✅ **احذف التوكن القديم عند انتهاؤه**

---

## ❓ إذا لم ينجح:

### المشكلة: "Authentication failed"

```bash
# امسح بيانات المصادقة القديمة:
git credential reject
# ثم حاول مرة أخرى
```

### المشكلة: "Permission denied"

```bash
# تأكد من أن التوكن له صلاحيات repo:
# https://github.com/settings/tokens
```

### المشكلة: "Repository not found"

```bash
# تأكد من:
# 1. اسم المستودع صحيح
# 2. المستودع عام (Public)
# 3. الـ URL صحيح
```

---

## 📋 الخطوات السريعة (ملخص):

1. ✅ اذهب إلى: https://github.com/settings/tokens
2. ✅ أنشئ Personal Access Token
3. ✅ انسخ التوكن
4. ✅ استخدمه كـ password عند الطلب
5. ✅ رفع الملفات!

---

## 🎯 بعد حل 2FA:

عندما تنجح في رفع الملفات:

1. **حدّث الأوراق البحثية:**
   ```
   استبدل: [GitHub Link - To be provided by author]
   بـ: https://github.com/mubtakir/tsp-geoattention
   ```

2. **قدم الورقة البحثية للمجلة**

3. **شارك المشروع مع المجتمع**

---

**استمتع بالنشر الأكاديمي! 🚀**

