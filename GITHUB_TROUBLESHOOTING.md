# 🔧 استكشاف الأخطاء - مشكلة المستودع

## ❌ الخطأ:
```
remote: Repository not found.
fatal: repository 'https://github.com/baserah-ai/tsp-geoattention.git/' not found
```

---

## ✅ الحل:

### الخطوة 1: تحقق من المستودع على GitHub

1. اذهب إلى: https://github.com/baserah-ai
2. تأكد من وجود مستودع باسم: `tsp-geoattention`
3. إذا لم يكن موجوداً، أنشئه:
   - اذهب إلى: https://github.com/new
   - الاسم: `tsp-geoattention`
   - الوصف: `TSP-GeoAttention - Hybrid Practical Approach`
   - اختر: **Public**
   - اضغط: **Create repository**

### الخطوة 2: تحقق من التوكن

التوكن الخاص بك:
```
[استخدم التوكن الخاص بك]
```

**تأكد من:**
- ✅ التوكن صحيح
- ✅ التوكن لم ينته (30 يوم)
- ✅ التوكن له صلاحيات `repo`

### الخطوة 3: جرب الرفع مرة أخرى

```bash
cd /home/al-mubtakir/Documents/p_np

# تحقق من الـ remote:
git remote -v

# إذا كان موجوداً، احذفه:
git remote remove origin

# أضف الـ remote الجديد:
git remote add origin https://github.com/baserah-ai/tsp-geoattention.git

# جرب الرفع:
git push -u origin main
```

عند الطلب:
- **Username:** mubtakir
- **Password:** [استخدم التوكن الخاص بك]

---

## 🔐 طريقة بديلة: استخدام SSH

إذا استمرت المشكلة، استخدم SSH:

```bash
# 1. أنشئ SSH key (إذا لم تكن موجودة):
ssh-keygen -t ed25519 -C "baserah-ai@github.com"

# 2. أضفه إلى GitHub:
# https://github.com/settings/keys

# 3. غيّر الـ remote:
git remote remove origin
git remote add origin git@github.com:baserah-ai/tsp-geoattention.git

# 4. جرب الرفع:
git push -u origin main
```

---

## 📋 قائمة التحقق:

- [ ] المستودع موجود على GitHub
- [ ] اسم المستودع صحيح: `tsp-geoattention`
- [ ] المستودع عام (Public)
- [ ] التوكن صحيح
- [ ] التوكن لم ينته
- [ ] التوكن له صلاحيات `repo`
- [ ] الـ remote صحيح

---

## 💡 نصائح:

1. **تحقق من الـ remote:**
   ```bash
   git remote -v
   ```

2. **اختبر الاتصال:**
   ```bash
   git ls-remote origin
   ```

3. **شاهد السجل:**
   ```bash
   git log --oneline
   ```

---

**بعد حل المشكلة، جرب الرفع مرة أخرى!**

