from  django.db.models import IntegerChoices

class Semester(IntegerChoices):
    FIRST_SEMESTER = 1, '1st Term'
    SECOND_SEMESTER = 2, '2nd Term'


class Role(IntegerChoices):
    ADMIN = 1, 'Admin'
    TEACHER = 2, 'Teacher'

class YearLevel(IntegerChoices):
    FIRST_YEAR = 1, 'First Year'
    SECOND_YEAR = 2, 'Second Year'
    THIRD_YEAR = 3, 'Third Year'
    FOURTH_YEAR = 4, 'Fourth Year'
    FIFTH_YEAR = 5, 'Fifth Year'


class Gender(IntegerChoices):
    MALE = 0, 'Male'
    FEMALE = 1, 'Female'

class EducationType(IntegerChoices):
    MALE_ONLY = 0, 'Male Only'
    FEMALE_ONLY = 1, 'Female Only'
    COEDUCATION = 2, 'Co-education'
    


class QuestionType(IntegerChoices):
    MULTIPLE_CHOICE = 1, 'Multiple Choice'
    TRUE_OR_FALSE = 2, 'True or False'

class QuestionDifficulty(IntegerChoices):
    EASY = 1, 'Easy'
    MEDIUM = 2, 'Medium'
    Difficult = 3, 'Difficult'


class AcademicYearStatus(IntegerChoices):
    FINISHED = 1, 'FINISHED'
    CURRENT = 2, 'CURRENT'
    UPCOMING = 3, 'Upcoming'

class QuizSessionStatus(IntegerChoices):
    LIVE = 1, 'Live'
    UPCOMING = 2, 'Upcoming'
    READY = 3, 'Ready'
    FINISHED = 4, 'Finished'

class QuizStatus(IntegerChoices):
    PUBLISHED = 1, 'Published'
    DRAFT = 2, 'Draft'
    READY = 3, 'Ready to Live'
    LIVE = 4, 'Live'
    FINISHED = 5, 'Finished'

class QuizStudentStatus(IntegerChoices):
    PASS = 1, 'Pass'
    FAIL = 2, 'Fail'
    ABSENT = 3, 'Absent'
    UPCOMING = 4, 'Upcoming'
    