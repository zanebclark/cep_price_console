# import pandas as pd
# df = pd.DataFrame({
#     'dogs': [1, 2, 3, 4],
#     'cost': [250, 150, 100, 40],
#     'revenue': [100, 250, 300, 100],
#     'cats': [100, 250, 300, 100]},
#     index=['A', 'B', 'C', 'D'])
# print(df)
#
# df_multindex = pd.DataFrame({'cost': [250, 150, 100, 5, 150, 300, 220, 7],
#                             'revenue': [100, 250, 300, 1, 200, 175, 225, 9]},
#                             index=[['Q1', 'Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', 'Q2'],
#                                    ['A', 'B', 'C', 'E', 'A', 'B', 'C', 'E']])
# print(df_multindex)
# print(df.eq(df_multindex, level=1, axis=0))
# print(df.eq(df_multindex, level=1, axis=1))