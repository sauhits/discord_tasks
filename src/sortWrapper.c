// sortWrapper.c
// Input: list [(int,string)]=[(deadline.title)]
// Output: list [(int,string)]=[(deadline.title)]

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern void printList(int n, char *list[n]);
int compare(const void *a, const void *b);
extern void sort(int n, char *list[n]);

void printList(int n, char *list[n])
{
    for (int i = 0; i < n; i++)
    {
        printf("%s\n", list[i]);
        char *ptr = strtok(list[i], ".");
        printf("%s\n", ptr);
    }
}

int compare(const void *a, const void *b)
{
    const char *str1 = *(const char **)a;
    const char *str2 = *(const char **)b;
    char deadline1[9], deadline2[9];
    sscanf(str1, "%8[^.].%*s", deadline1);
    sscanf(str2, "%8[^.].%*s", deadline2);
    return strcmp(deadline1, deadline2);
}

// リストをソートして返す関数
char **sortList(int n, char *list[n])
{
    // ソート用にメモリをコピー
    char **sorted_list = malloc(n * sizeof(char *));
    for (int i = 0; i < n; i++)
    {
        sorted_list[i] = strdup(list[i]);
    }
    // ソート実行
    qsort(sorted_list, n, sizeof(char *), compare);
    // ソート結果を返す
    return sorted_list;
}

// ソート結果を解放する関数
void freeList(int n, char *list[n])
{
    for (int i = 0; i < n; i++)
    {
        free(list[i]);
    }
    free(list);
}