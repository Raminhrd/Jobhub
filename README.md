🏢 Recruitment System Django Project
A complete recruitment management system built with Django REST Framework, designed for managing job applications, capacity tracking, and automatic candidate categorization.

🚀 Features

✅ Job Management

Admins can create, edit, and delete job positions.

Each job has a capacity, start & end time, and automatic remaining capacity tracking.

✅ Candidate Registration

Candidates can register for only one job position.

They can view open jobs (capacity available and within date range).

After registration, the system automatically reduces the job’s remaining capacity.

A candidate can change their job only within 24 hours of registration.

✅ Admin Dashboard

View all candidates grouped by job and category.

Automatically distribute candidates into three homogeneous groups based on their education level and GPA.

Manually edit or delete candidate registrations.

✅ Job Basket System

Works like a shopping cart users “add” a job to their basket.

Prevents duplicate or expired job registrations.

⚙️ Tech Stack
Tool	Description
🐍 Python	Core programming language
🎯 Django	Web framework
🧩 Django REST Framework (DRF)	API development
🕓 Timezone-aware logic	For registration and deadlines
🧠 Smart Categorization Algorithm	Automatic candidate grouping
🗄️ SQLite / PostgreSQL	Database support
🧱 Database Models

🧩 API Endpoints
Method	Endpoint	Description
GET	/recruitment/job-list/	List all jobs
POST	/recruitment/job-list/	Create new job (Admin only)
POST	/recruitment/add-job/<job_id>/	Add job to candidate basket
GET	/recruitment/my-job/	View candidate’s selected job
POST	/recruitment/auto-categorize/<job_id>/	Auto categorize candidates
GET	/recruitment/grouped-candidates/<job_id>/	View grouped candidates (Admin only)
🔐 Access Control

👨‍💻 Admin

Can create/edit/delete jobs

Can categorize and view all candidates

👤 User

Can register once, view available jobs, and edit within 24 hours

💡 Future Improvements

 Add JWT authentication

 Create admin dashboard (React / Vue)

 Export candidate reports (PDF / Excel)

 Notifications when registration time ends

🧠 Author

Ramin Hosseinirad
🎯 Backend Developer | Python & Django Enthusiast
☕ Powered by coffee & clean code.
