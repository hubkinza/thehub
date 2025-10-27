A modern, discussion platform where users can share ideas, engage in conversations, and build a community.

🔗 Live Site: http://13.49.238.130

## Introduction

**The Hub** is a discussion-based blog platform designed to facilitate meaningful conversations on topics that matter. Users can create posts, comment on discussions, like content, and search through topics of interest.

The platform features role-based access control with admin capabilities for content moderation.

### Key Features

- **User Authentication** - Secure registration and login system with password hashing
- **Post Creation** - Rich text discussions with tagging functionality
- **Add Tags** - Rich text discussions with tagging functionality
- **Comments System** - commenting on all posts
- **Like System** - Engage with content through likes
- **Search Functionality** - search discussions by title, content, or tags
- **Admin Panel** - Administrative controls for content moderation
- **Responsive Design** - Mobile-friendly interface with modern UI/UX

### Technologies Used

**Backend:**

- Python
- Flask 3.0.0
- PostgreSQL (AlwaysData)
- SQLAlchemy (ORM)

**Frontend:**

- HTML5
- CSS

**Deployment:**

- AWS
# 🎨 UI/UX Design

### Design Philosophy
The Hub embraces a clean, minimalist aesthetic with a focus on readability and user engagement. The design prioritizes content while maintaining visual appeal through subtle decorative elements and a warm color palette.

### Color Palette
- **Primary Background:** `#FFF8F0` (Warm cream)
- **Text Primary:** `#2C1810` (Dark brown)
- **Accent Color:** `#8B4513` (Saddle brown)
- **Interactive Elements:** `#FF6B35` (Orange)
- **Admin Actions:** `#DC3545` (Red)

### Typography
- **Headings:** Georgia, serif
- **Body Text:** -apple-system, system-ui (System fonts for optimal performance)
- **Emphasis on readability** with appropriate line heights and letter spacing

### Key Design Elements
- **Decorative Corner Ornaments** - Unique visual identity on headers
- **Card-based Layout** - Clean separation of content
- **Responsive Grid System** - Adapts seamlessly across devices
- **Visual Feedback** - Hover states, loading indicators, and success messages

### User Experience Considerations
- **Fast Load Times** - Optimized assets and minimal dependencies
- **Accessibility** - Semantic HTML and proper contrast ratios
- **Clear Hierarchy** - Visual weight guides user attention
- **Consistent Patterns** - Familiar UI patterns reduce cognitive load

---

## 👥 User Stories

### As a First-Time Visitor
- I want to see the latest discussions on the homepage so I can gauge the community's interests
- I want to easily understand what the platform offers so I can decide if I want to join
- I want a simple registration process so I can quickly become a member

### As a Registered User
- I want to create posts with titles, content, and tags so I can share my thoughts with the community
- I want to comment on other users' posts so I can engage in discussions
- I want to like posts that resonate with me so I can show appreciation
- I want to search for specific topics so I can find relevant discussions
- I want to see how many people have engaged with my posts (likes and comments)
- I want my session to persist so I don't have to log in repeatedly

### As an Administrator
- I want to delete any post that violates community guidelines so I can maintain platform quality
- I want clear visual indicators of my admin status so I know when I'm using admin powers
- I want to view all users posts so I can moderate effectively
- I want confirmation prompts before deleting content to prevent accidental removals

### As a Content Creator
- I want my posts to be searchable by tags so others can discover my content
- I want to edit my posts after publishing to correct mistakes or add information

---
### Desktop Views
<img width="2934" height="1598" alt="image" src="https://github.com/user-attachments/assets/f5d4251d-c6fe-4907-8e60-e70c35358e40" />

### Tablet View
<img width="1248" height="1546" alt="image" src="https://github.com/user-attachments/assets/62514942-1cba-4467-bd92-79af9a629d50" />
### Mobile Views
<img width="1248" height="1598" alt="image" src="https://github.com/user-attachments/assets/f9f86ecd-a86a-4fac-85e0-2fde4b87b25a" />


**Database structure**
![ERD](static/readme/database.png)

## 🧪 Manual Testing

### Test Cases

| Test Case | Description | Steps | Expected Result | Status |
|-----------|-------------|-------|-----------------|--------|
| **TC01** | User Registration | 1. Navigate to /register.html<br>2. Enter username, email, password<br>3. Confirm password<br>4. Click "Register Account" | User account created, redirected to discussions page, session established | ✅ Pass |
| **TC02** | User Login | 1. Navigate to /login.html<br>2. Enter valid email and password<br>3. Click "Sign In" | User logged in, redirected to discussions page | ✅ Pass |
| **TC03** | Login with Invalid Credentials | 1. Navigate to /login.html<br>2. Enter incorrect email/password<br>3. Click "Sign In" | Error message displayed: "Invalid email or password" | ✅ Pass |
| **TC04** | Create Post | 1. Login as user<br>2. Click "Start Discussion"<br>3. Enter title, content, tags<br>4. Click "Publish Discussion" | Post created, appears in discussions list | ✅ Pass |
| **TC05** | View Post | 1. Navigate to discussions<br>2. Click "Join the Conversation" on any post | Post details displayed with content, author, date, tags | ✅ Pass |
| **TC06** | Add Comment | 1. Open a post<br>2. Enter comment text<br>3. Click "Post Comment" | Comment added, appears in comments list | ✅ Pass |
| **TC07** | Like Post (Toggle On) | 1. Login as user<br>2. Click heart icon on post | Like count increases by 1, heart fills | ✅ Pass |
| **TC08** | Unlike Post (Toggle Off) | 1. Click heart icon on previously liked post | Like count decreases by 1, heart unfills | ✅ Pass |
| **TC09** | Search Functionality | 1. Navigate to discussions<br>2. Type keyword in search box | Posts filter in real-time to match search query | ✅ Pass |
| **TC10** | Admin Login | 1. Navigate to /login.html<br>2. Enter admin@thehub.com / admin123<br>3. Click "Sign In" | Admin logged in, admin privileges active | ✅ Pass |
| **TC11** | Admin Delete Post | 1. Login as admin<br>2. Navigate to discussions<br>3. Click "🗑️ Admin Delete" on any post<br>4. Confirm deletion | Post deleted, removed from list | ✅ Pass |
| **TC12** | Regular User Cannot Delete | 1. Login as regular user<br>2. Navigate to discussions | No delete buttons visible on any posts | ✅ Pass |
| **TC13** | Logout Functionality | 1. Click "Logout" in navigation | Session cleared, redirected to logout page | ✅ Pass |
| **TC14** | Protected Route Access | 1. Logout<br>2. Try to access /discussions.html directly | Redirected to login page | ✅ Pass |
| **TC15** | Empty Search Results | 1. Search for non-existent term | "No discussions found" message displayed | ✅ Pass |
| **TC17** | Responsive Design - Mobile | 1. Open site on mobile device<br>2. Navigate through pages | Layout adjusts, elements stack vertically, touch-friendly | ✅ Pass |
| **TC18** | Responsive Design - Tablet | 1. Open site on tablet (768px)<br>2. Test all pages | Layout optimized for medium screens | ✅ Pass |
| **TC19** | Form Validation - Empty Fields | 1. Try to submit forms with empty required fields | Error messages displayed, form not submitted | ✅ Pass |
| **TC20** | Password Mismatch | 1. Register with non-matching passwords | Alert: "Passwords do not match!" | ✅ Pass |
| **TC21** | Duplicate Email Registration | 1. Try to register with existing email | Error: "Email already registered" | ✅ Pass |
| **TC24** | Database Connection | 1. Start application<br>2. Check Flask logs | PostgreSQL connection established, no errors | ✅ Pass |

### Browser Compatibility Testing

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome | 120+ | ✅ Pass | Fully functional |
| Firefox | 121+ | ✅ Pass | Fully functional |
| Safari | 17+ | ✅ Pass | Fully functional |
| Edge | 120+ | ✅ Pass | Fully functional |

### Device Testing

| Device Type | Screen Size | Status | Notes |
|-------------|-------------|--------|-------|
| Desktop | 1920x1080 | ✅ Pass | Optimal viewing experience |
| Laptop | 1366x768 | ✅ Pass | All content visible |
| Tablet (iPad) | 768x1024 | ✅ Pass | Responsive adjustments work |
| Mobile (iPhone 14) | 390x844 | ✅ Pass | Mobile-optimized layout |


### Automated testing 
## CSS Validator
![ERD](static/readme/CSS.png)
## JSHINT
![ERD](static/readme/js.png)

---

