-- Схема: Университет (MySQL)

CREATE TABLE faculties (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE departments (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT UNSIGNED,
    name VARCHAR(100) NOT NULL UNIQUE,
    parent_id INT UNSIGNED,
    FOREIGN KEY (faculty_id) REFERENCES faculties(id),
    FOREIGN KEY (parent_id) REFERENCES departments(id)
) ENGINE=InnoDB;

CREATE TABLE teachers (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    degree VARCHAR(50),
    position VARCHAR(100),
    FOREIGN KEY (department_id) REFERENCES departments(id)
) ENGINE=InnoDB;

CREATE TABLE `groups` (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED,
    name VARCHAR(20) NOT NULL UNIQUE,
    course INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
) ENGINE=InnoDB;

CREATE TABLE students (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    group_id INT UNSIGNED,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    enrollment_year INT NOT NULL,
    scholarship DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (group_id) REFERENCES `groups`(id)
) ENGINE=InnoDB;

CREATE TABLE courses (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNSIGNED,
    name VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    semester INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
) ENGINE=InnoDB;

CREATE TABLE course_teachers (
    course_id INT UNSIGNED,
    teacher_id INT UNSIGNED,
    PRIMARY KEY (course_id, teacher_id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
) ENGINE=InnoDB;

CREATE TABLE course_groups (
    course_id INT UNSIGNED,
    group_id INT UNSIGNED,
    PRIMARY KEY (course_id, group_id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (group_id) REFERENCES `groups`(id)
) ENGINE=InnoDB;

CREATE TABLE classrooms (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    building VARCHAR(50),
    room_number VARCHAR(10) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE schedule (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id INT UNSIGNED,
    group_id INT UNSIGNED,
    teacher_id INT UNSIGNED,
    classroom_id INT UNSIGNED,
    lesson_date DATE NOT NULL,
    lesson_time TIME NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (group_id) REFERENCES `groups`(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
) ENGINE=InnoDB;

CREATE TABLE exams (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id INT UNSIGNED,
    group_id INT UNSIGNED,
    exam_date DATE NOT NULL,
    classroom_id INT UNSIGNED,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (group_id) REFERENCES `groups`(id),
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
) ENGINE=InnoDB;

CREATE TABLE grades (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED,
    course_id INT UNSIGNED,
    exam_id INT UNSIGNED,
    grade VARCHAR(2) NOT NULL,
    graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id)
) ENGINE=InnoDB;

CREATE TABLE attendance (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED,
    schedule_id INT UNSIGNED,
    present TINYINT(1) DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (schedule_id) REFERENCES schedule(id)
) ENGINE=InnoDB;

CREATE TABLE publications (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT UNSIGNED,
    title VARCHAR(200) NOT NULL,
    published_at DATE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
) ENGINE=InnoDB;

CREATE TABLE events (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    event_date DATE NOT NULL,
    location VARCHAR(200)
) ENGINE=InnoDB;

CREATE TABLE event_participants (
    event_id INT UNSIGNED,
    student_id INT UNSIGNED,
    PRIMARY KEY (event_id, student_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
) ENGINE=InnoDB;

CREATE TABLE applications (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED,
    type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
) ENGINE=InnoDB;

CREATE TABLE messages (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sender_id INT UNSIGNED,
    receiver_id INT UNSIGNED,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sender_type VARCHAR(20) NOT NULL,
    receiver_type VARCHAR(20) NOT NULL
) ENGINE=InnoDB;
