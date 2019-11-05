#!/usr/bin/env python
# coding: utf-8

# In[160]:


from stackapi import StackAPI, StackAPIError
#passing website and key
SITE = StackAPI('stackoverflow',key='1m2D1EmsS*nKHGMwKBEAgQ((')
SITE.max_pages=5
SITE.page_size=100
#calling questions API to get questions wtagged with Java and sorted by votes
questions = SITE.fetch('questions', sort='votes',tagged='java')

#passing all question ids into a array
question_id = []
for i in (questions['items']):
    question_id.append(i['question_id'])


# In[162]:


answer = []
#calling API to get all answers of the questions by passing question ids
for i in question_id:
    ans = SITE.fetch('questions/{0}/answers/'.format(i))
    answer.append(ans)
print(len(answer))

#getting all question ids of the answers
quest_ids = []
ans_data =[]
for i in range(300):
    d = questions['items'][i]
    ans_data.append(questions['items'][i])
    quest_ids.append(d['question_id'])


# In[194]:


#Passing all answers into an array as individuall answer rather than dict form
ind_ans = []
for i in quest_ids:
    for r in answer:
        for s in r['items']:
            if s['question_id'] == i:
                ind_ans.append(s)
print(len(ind_ans))


# In[195]:


import csv

#header defnition
def header(file,result):
    result =[]
    #header for all posts file
    if file == 'allposts':
        result.append('Tags'); result.append('Asker Reputation'); result.append('Asker Id')
        result.append('Asker Name');result.append('Link to Asker')
        result.append('Is Answered');result.append('View Count');result.append('Answer Count')
        result.append('Score');result.append('last_activity_date');result.append('creation_date')
        result.append('Question Id');result.append('link');result.append('Title')

        result.append('Answerer Reputation');result.append('Answerer Id');result.append('user_type');
        result.append('Answerer Name')
        result.append('Answerer Prof Link');result.append('Is Accepted'); result.append('Answer Score');
        result.append('Last Activity data');result.append('Last Edited date');result.append('Creation date');
        result.append('Answer Id')
    #header for meta_data file
    elif (file == 'meta_data'):
        result.append('Asker Id');result.append('Post_link');result.append('Answerer Id')
    #header for ask_ans file
    elif (file == 'ask_ans'):
            result.append('Asker Id');result.append('Answerer Id')
    return(result)
        
#Appendinf all questions
def get_ques(var,file):
    result = []
    qown = var['owner']
    if file == 'allposts':
        tags = var['tags']; 
        result.append(tags)
        ask_rep = qown['reputation'];result.append(ask_rep)
        asker_id = qown['user_id']; result.append(asker_id)
        asker_na = qown['display_name']; result.append(asker_na)
        link_p = qown['link']; result.append(link_p)
        is_ans = var['is_answered'];result.append(is_ans)
        q_view = var['view_count']; result.append(q_view)
        answer_c = var['answer_count']; result.append(answer_c)
        qscore = var['score']; result.append(qscore)
        last_act = var['last_activity_date']; result.append(last_act)
        creat_d = var['creation_date']; result.append(creat_d)
        qid = var['question_id'];result.append(qid)
        link = var['link']; result.append(link)
        title = var['title'];result.append(title)
    elif (file == 'meta_data'):
        asker_id = qown['user_id']; result.append(asker_id)
        link = var['link']; result.append(link)
    elif (file == 'ask_ans'):
            asker_id = qown['user_id']; result.append(asker_id)
    return(result)

#Appending all answers
def get_ans(i,val,file,tsvout):
    result = get_ques(i,file)
    aown = val['owner']
    if file == 'allposts':
        ansr_rep = aown['reputation'];result.append(ansr_rep)
        ansr_id = aown['user_id'];result.append(ansr_id)
        ansr_type = aown['user_type'];result.append(ansr_type)
        ansr_name = aown['display_name'];result.append(ansr_name)
        ansr_type = aown['user_type'];result.append(ansr_type)
        ansr_link = aown['link'];result.append(ansr_link)
        is_acc = val['is_accepted'];result.append(is_acc)
        ans_score = val['score'];result.append(ans_score)
        last_ac = val['last_activity_date'];result.append(last_ac)
        cre_d = val['creation_date']; result.append(cre_d)
        ans_id = val['answer_id']; result.append(ans_id)
        tsvout.writerow(result)
    else:
        ansr_id = aown['user_id'];result.append(ansr_id)
        tsvout.writerow(result)


# In[196]:


#main function defnition
def main(file):
    import csv
    result = []
    #opening and writing the fetched data into out.tsv file
    with open('C:/Users/Akhil/Desktop/out.tsv', 'w',encoding='utf-8') as tsvout:
        result = header(file,result);
        tsvout = csv.writer(tsvout, delimiter = '\t')
        #writing header
        tsvout.writerow(result)
        #getting data where the questions and answers having same question_id and appending
        for i in ans_data:
            for j in ind_ans:
                if i['question_id'] == j['question_id']:
                    q_own = j['owner'];a_own = i['owner']
                    #exclusion of users who are not registered
                    if q_own['user_type'] == 'does_not_exist' or a_own['user_type'] == 'does_not_exist':
                        continue
                    get_ans(i,j,file,tsvout)
#             break
    print('{0}.tsv file generated'.format(file))


# In[200]:


main('allposts')
main('meta_data')
main('ask_ans')

