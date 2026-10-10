
# 🖼️ Assets & Images Usage Guide

## 🔍 Why We Use External Image Links

Instead of storing large image files inside the `frontend/assets/` folder, this project uses direct image URLs from the web. This helps:

- ✅ Save disk space and Docker image size
- ✅ Avoid cluttering the repository with unnecessary media
- ✅ Quickly test different design ideas without re-uploading images
- ✅ Speed up prototyping and reduce build time

---

## 🌐 How to Use Image Links

1. **Go to Google Images**
2. Search for a suitable background or icon
3. Right-click on the image and choose **"Open image in new tab"**
4. Copy the **direct URL** from the browser address bar
5. Use it directly in your CSS like this:

```css
background: url('https://img.freepik.com/free-photo/abstract-gradient-neon-lights_23-2149279141.jpg') no-repeat center center fixed;
````

---

## 📁 Example URLs Used in This Project

* 🔗 Background:
  `https://img.freepik.com/free-photo/abstract-gradient-neon-lights_23-2149279141.jpg`

* 🔗 Alternate Option:
  `https://img.freepik.com/free-photo/abstract-neon-laser-lights_23-2149327391.jpg`

> These are free assets sourced from [Freepik](https://www.freepik.com), which allows non-commercial use with attribution.

---

## 📌 Notes

* Ensure image URLs are **permanent and publicly accessible**
* Avoid copyrighted or unstable image links
* You can always switch to local assets later if needed

```
