import rules
from icecream import ic
from core.constants import Role


@rules.predicate
def is_teacher(user):
    ic(rules.is_authenticated)
    return user.role == Role.TEACHER


# @rules.predicate
# def is_student(user):
#     return user.role == Role.STUDENT

# @rules.predicate
# def is_quiz_teacher(user, quiz):
#     return ic(quiz.quiz_for.filter(teacher=user.teacher).exists())


# rules.add_perm('quiz.can_view', is_teacher & rules.is_authenticated )

# rules.add_perm('quiz.can_edit', is_quiz_teacher & rules.is_authenticated)



# @rules.predicate
# def is_quiz_teacher(user, quiz):
#     return quiz.quiz_for.filter(teacher=user.teacher).exists()

# rules.add_rule("is_teacher", is_teacher)
# rules.add_rule("is_quiz_teacher", is_quiz_teacher)
# rules.add_perm('quiz.can_view', is_teacher)

# teacher_rule_set = rules.RuleSet(
#     name="teacher",
#     predicates={
#         "is_teacher": is_teacher,
#         "is_quiz_teacher": is_quiz_teacher,
#     },
#     rules={
#         "can_add_quiz": rules.is_authenticated & is_teacher,
#         "can_edit_quiz": rules.is_authenticated & is_teacher & is_quiz_teacher,
#         "can_delete_quiz": rules.is_authenticated & is_teacher & is_quiz_teacher,
#     },
# )
