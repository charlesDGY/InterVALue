
;; Function add (add, funcdef_no=2, decl_uid=2693, cgraph_uid=2)

add (int a, int b)
{
  __builtin_putchar (10);
  return;
}



;; Function sub (sub, funcdef_no=3, decl_uid=2702, cgraph_uid=3)

sub (int a, int b)
{
  int d;
  int D.2729;

  d = a - b;
  D.2729 = d;
  goto <D.2730>;
  <D.2730>:
  return D.2729;
}



;; Function main (main, funcdef_no=4, decl_uid=2706, cgraph_uid=4)

main (int i)
{
  char ma;
  int k;
  int haha;
  int j;
  int * point;
  int * kk;
  struct node2 * node44;
  int j;
  int val2;
  int val;
  int D.2745;
  int D.2744;
  int D.2739;
  int D.2732;
  int D.2731;

  val = 12;
  val2 = 6;
  j = 32767;
  D.2731 = val + val2;
  D.2732 = D.2731 * val2;
  j = D.2732 - val;
  if (i > 0) goto <D.2735>; else goto <D.2733>;
  <D.2735>:
  if (j <= 49) goto <D.2736>; else goto <D.2733>;
  <D.2736>:
  goto <D.2712>;
  <D.2711>:
  j = j + 5;
  <D.2712>:
  if (j <= 99) goto <D.2711>; else goto <D.2713>;
  <D.2713>:
  goto <D.2734>;
  <D.2733>:
  j = j + -1;
  <D.2734>:
  if (val == 5) goto <D.2737>; else goto <D.2738>;
  <D.2737>:
  val = val + 1;
  val2 = val % 2;
  <D.2738>:
  node44 = 0B;
  node44->p = 5;
  node44->j = 10;
  kk = malloc (4);
  *kk = 5;
  point = kk;
  D.2739 = *point;
  if (D.2739 != 5) goto <D.2740>; else goto <D.2741>;
  <D.2740>:
  __builtin_putchar (10);
  <D.2741>:
  j = 5;
  haha = 10;
  if (k == 4) goto <D.2742>; else goto <D.2743>;
  <D.2742>:
  __builtin_putchar (10);
  <D.2743>:
  D.2744 = add (i, j);
  val = sub (D.2744, val);
  goto <D.2726>;
  <D.2725>:
  switch (val) <default: <D.2724>, case 3: <D.2721>, case 8: <D.2723>>
  <D.2721>:
  sub (i, j);
  goto <D.2722>;
  <D.2723>:
  add (i, j);
  j = 6;
  goto <D.2722>;
  <D.2724>:
  i = 5;
  <D.2722>:
  <D.2726>:
  if (i > 0) goto <D.2725>; else goto <D.2727>;
  <D.2727>:
  printf ("%d\n", j);
  D.2745 = 0;
  goto <D.2746>;
  <D.2746>:
  return D.2745;
}


