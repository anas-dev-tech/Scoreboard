from django.apps import apps
from .constants import Role, Semester, QuestionType, QuestionDifficulty, YearLevel, StudentGroupNumber
from faker import Faker
import random
from icecream import ic


StudentGroup = apps.get_model('users', 'StudentGroup')
Course = apps.get_model('academics', 'Course')
Teacher = apps.get_model('users', 'Teacher')
AcademicYear = apps.get_model('academics', 'AcademicYear')
Syllabus = apps.get_model('academics', 'CourseAssignment')
Quiz = apps.get_model('quiz', 'Quiz')
Question = apps.get_model('quiz', 'Question')
QuestionOption = apps.get_model('quiz', 'QuestionOption')
Major = apps.get_model('academics', 'Major')
Student = apps.get_model('users', 'Student')



def fake_data_for_course():
    courses = [
        # IT Courses
        "Introduction to Information Systems",
        "Database Management Systems",
        "Network Security",
        "Cybersecurity",
        "Cloud Computing",
        "Data Science",
        "Business Intelligence",
        "Software Engineering",
        "IT Project Management",
        "IT Service Management",
        "Digital Forensics",
        "Information Systems Audit and Control",

        # CS Courses
        "Algorithms and Data Structures",
        "Programming Fundamentals (Python, Java, C++)",
        "Operating Systems",
        "Computer Architecture",
        "Artificial Intelligence",
        "Machine Learning",
        "Software Development Methodologies",
        "Web Development",
        "Mobile App Development",
        "Database Systems",
        "Computer Networks",
        "Human-Computer Interaction",
        "Data Mining",
        "Computer Graphics",

        # IS Courses
        "Information Systems Analysis and Design",
        "Management Information Systems",
        "Decision Support Systems",
        "E-commerce",
        "Digital Marketing",
        "Project Management",
        "Systems Analysis and Design",
        "Business Process Reengineering",
        "Enterprise Resource Planning (ERP)",
        "Supply Chain Management",

        # Graphics Courses
        "3D Modeling and Animation",
        "Game Development",
        "Digital Painting and Illustration",
        "Graphic Design",
        "UX/UI Design",
        "Video Editing",
        "Motion Graphics",
        "Web Design",
        "Interactive Media Design",
        "Visual Effects"
    ]

    # Assuming you have a Course model with fields 'name' and 'category'
    Course = apps.get_model('academics', 'Course')
    majors = Major.objects.all()
    for course_name in courses:
        major=random.choice(majors)
        
        Course.objects.create(
            name=course_name,
            year_level=random.choice(YearLevel.choices)[0],
            major=major
        )
        

def fake_data_for_student(num_records=100, group_id=None):
    fake = Faker()
    if group_id is None:
        student_groups = StudentGroup.objects.all()
    else:
        student_groups = StudentGroup.objects.filter(id=group_id)
        
        
    
    for _ in range(num_records):
        for group in student_groups:
            Student.objects.create(
                id=fake.unique.random_number(digits=10),
                name=fake.name(),
                group=group,
            )
        

def fake_data_for_teacher(num_users=10):
    fake = Faker()
    User = apps.get_model('users', 'User')
    Teacher = apps.get_model('users', 'Teacher')
    for _ in range(num_users):
        user = User(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email=fake.email(),
            role=Role.TEACHER # Get the key from choices tuple
        )
        user.set_password('Anas775995183')
        user.save()
        print('user:', user)

def fake_data_for_syllabus(num_records=10):
    """Populates the Syllabus model with fake data, selecting from existing foreign key objects."""

    fake = Faker()

    for _ in range(num_records):
        try:
            # Select random existing objects
            student_group = StudentGroup.objects.order_by('?').first()
            course = Course.objects.order_by('?').first()
            teacher = Teacher.objects.order_by('?').first()
            academic_year = AcademicYear.objects.order_by('?').first()
            semester = fake.random_int(1, 2)  # Assuming semesters are 1 or 2

            # Create a new Syllabus object
            syllabus = Syllabus.objects.create(
                student_group=student_group,
                course=course,
                teacher=teacher,
                academic_year=academic_year,
                semester=semester,
            )

            print(f"Created Syllabus: {syllabus}")
        except Exception as e:
            print(f"Error creating Syllabus: {e}")








def generate_fake_data_for_quizzes(q_num):
    faker = Faker()
    question_num = q_num
    # Fetch all existing quizzes
    quizzes = Quiz.objects.all()

    for quiz in quizzes:
        print(f'Populating quiz: {quiz.title}')

        # Create a random number of questions for each quiz
        for _ in range(question_num):
            question_type = random.choice([QuestionType.TRUE_OR_FALSE, QuestionType.MULTIPLE_CHOICE])
            question_difficulty = random.choice(QuestionDifficulty.choices)[0]

            question = Question.objects.create(
                text=faker.sentence(nb_words=6),
                quiz=quiz,
                score=round(random.uniform(1, 5), 2),
                question_difficulty=question_difficulty,
                question_type=question_type
            )

            # Create options based on question type
            if question_type == QuestionType.TRUE_OR_FALSE:
                QuestionOption.objects.create(text='True', question=question)
                QuestionOption.objects.create(text='False', question=question)
            else:
                num_options = random.randint(3, 5)
                for _ in range(num_options):
                    QuestionOption.objects.create(
                        text=faker.sentence(nb_words=2),
                        question=question
                    )

            # Randomly select the correct answer
            question.answer = random.choice(question.question_options.all())
            question.save()

        print(f'Quiz "{quiz.title}" populated with questions and options.')


def fake_data_for_student_group():
    """Populates the StudentGroup model with fake data."""
    # Create fake data for StudentGroup
    majors = Major.objects.all()
    for major in majors:
        for year_level in range(1,5):
            for group_number in range(1,4):
                for type in range(1,4):
                    try:
                        StudentGroup.objects.create(
                            major=major,
                            year_level=year_level,
                            number=group_number,
                                education_type=type
                                )
                        # Print the created StudentGroup object
                        print(f"Created StudentGroup: {StudentGroup}")
                    except Exception as e:
                        print(f"Error creating StudentGroup: {e}")


def fake_data_for_syllabus(syllabus_num):
    course = Course.objects.all()
    teacher = Teacher.objects.all()
    student_groups = StudentGroup.objects.all()
    
    for student_group in student_groups:
        try:
            # Generate random data for the Syllabus object
            ic(course)
            course = course.filter(major=student_group.major, year_level=student_group.year_level)
            course = random.choice(course)
            teacher = random.choice(teacher)
            
            # Create the Syllabus object
            syllabus = Syllabus.objects.create(
                course=course,
                teacher=teacher,
                student_group=student_group
            )
            syllabus.save()
            
            print(f"Created Syllabus: {syllabus}")
        except Exception as e:
            print(f"Error creating Syllabus: {e}")
            
            