import uiautomator2 as u2
import time
import sys

# === CONFIGURATION ===
HASHTAG = "examplehashtag"  # Don't include the "#" when searching
MAX_SCROLLS = 5
AUTO_LIKE = True

# === CONNECT TO DEVICE ===
print("[...] Connecting to device...")
try:
    d = u2.connect()
    print(f"[✔] Connected to device: {d.device_info['model']}")
except Exception as e:
    print(f"[✘] Failed to connect to device: {e}")
    sys.exit(1)

# === LAUNCH INSTAGRAM ===
print("[...] Launching Instagram...")
d.app_start('com.instagram.android')
time.sleep(5)

# === SEARCH FOR HASHTAG ===
try:
    print(f"[...] Searching for #{HASHTAG}...")
    
    # Click on search (bottom navigation)
    search_btn = d(descriptionContains="Search")
    if not search_btn.wait(timeout=10):
        raise Exception("Search button not found.")
    search_btn.click()
    time.sleep(2)

    # Click on the search input and type hashtag
    search_field = d(resourceId="com.instagram.android:id/action_bar_search_edit_text")
    if not search_field.exists(timeout=5):
        raise Exception("Search field not found.")
    search_field.set_text(HASHTAG)
    d.press("enter")
    time.sleep(3)

    # Click on the first hashtag result
    tag_result = d(className="android.widget.TextView", textContains=HASHTAG)
    if not tag_result.wait(timeout=5):
        raise Exception("Hashtag result not found.")
    tag_result.click()
    time.sleep(5)

except Exception as e:
    print(f"[✘] Failed during hashtag search: {e}")
    sys.exit(1)

# === INTERACT WITH POSTS ===
likes = 0
print(f"[...] Scrolling and interacting with posts (max {MAX_SCROLLS})...")

for i in range(MAX_SCROLLS):
    print(f"→ Scroll #{i+1}")

    # Find first visible post (by clickable image container)
    post = d.xpath('//android.widget.ImageView').get()
    if post:
        post.click()
        time.sleep(3)

        if AUTO_LIKE:
            try:
                like_btn = d(descriptionContains="Like")
                if like_btn.exists:
                    like_btn.click()
                    likes += 1
                    print(f"[♥] Liked post #{likes}")
                else:
                    print("[!] Like button not found or already liked.")
            except Exception as e:
                print(f"[!] Error while liking: {e}")

        d.press("back")
        time.sleep(2)
    else:
        print("[!] No post found on screen.")

    # Scroll down
    d.swipe(0.5, 0.8, 0.5, 0.2)
    time.sleep(2)

print(f"[✔] Done! Total posts liked: {likes}")