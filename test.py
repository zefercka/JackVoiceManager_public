from execute_command import text_transform, nlp

t = text_transform("сколько ехать от пригородного шоссе до балашихи")
del_words = ['ехать', 'маршрут', 'построй', 'занимает', 'дорога', ]
for i in del_words:
    t = t.replace(i, "")

print(t)
# p_ = []
# for i in nlp(t):
#     print(str(i), i.pos_)
#     if i.pos_ == "PROPN":
#         p_.append(str(i))
#
# print(p_)