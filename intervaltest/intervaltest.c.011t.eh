
;; Function add (add, funcdef_no=2, decl_uid=2693, cgraph_uid=2)

add (int a, int b)
{
  int D.2739;

  __builtin_putchar (10);
  D.2739 = a + b;
  goto <D.2740>;
  <D.2740>:
  return D.2739;
}



;; Function sub (sub, funcdef_no=3, decl_uid=2704, cgraph_uid=3)

sub (int a, int b)
{
  long int d;
  int D.2742;
  int D.2741;

  D.2741 = a - b;
  d = (long int) D.2741;
  D.2742 = (int) d;
  goto <D.2743>;
  <D.2743>:
  return D.2742;
}



;; Function main (main, funcdef_no=4, decl_uid=2708, cgraph_uid=4)

main (int i)
{
  char ma;
  unsigned char pio;
  long unsigned int poi;
  unsigned int pp;
  float noha;
  short unsigned int k;
  float haha;
  double j;
  long int cao;
  int woca;
  float noteasy;
  int * point;
  int * kk;
  struct node2 * node44;
  int a[50];
  int j;
  int val2;
  int val;
  int D.2773;
  int j.9;
  int D.2771;
  int j.8;
  int D.2765;
  int D.2762;
  int j.7;
  int j.6;
  int j.5;
  int j.4;
  int j.3;
  int j.2;
  int j.1;
  int D.2748;
  int D.2747;
  float glob2.0;

  woca = 9;
  cao = 32;
  glob = 1;
  glob2.0 = glob2;
  if (glob2.0 == 4.5e+0) goto <D.2745>; else goto <D.2746>;
  <D.2745>:
  glob2 = 4.0e+0;
  <D.2746>:
  val = 12;
  val2 = 6;
  j = 32767;
  D.2747 = val + val2;
  D.2748 = D.2747 * val2;
  j.1 = D.2748 - val;
  j = j.1;
  if (i > 0) goto <D.2752>; else goto <D.2750>;
  <D.2752>:
  j.2 = j;
  if (j.2 <= 49) goto <D.2754>; else goto <D.2750>;
  <D.2754>:
  goto <D.2716>;
  <D.2715>:
  j.3 = j;
  j.4 = j.3 + 5;
  j = j.4;
  <D.2716>:
  j.5 = j;
  if (j.5 <= 99) goto <D.2715>; else goto <D.2717>;
  <D.2717>:
  goto <D.2751>;
  <D.2750>:
  j.6 = j;
  j.7 = j.6 + -1;
  j = j.7;
  <D.2751>:
  if (val == 5) goto <D.2760>; else goto <D.2761>;
  <D.2760>:
  val = val + 1;
  val2 = val % 2;
  <D.2761>:
  a[10] = 100;
  a[39] = 23;
  a[val] = 4;
  D.2762 = a[10];
  if (D.2762 == 100) goto <D.2763>; else goto <D.2764>;
  <D.2763>:
  a[32] = 3;
  <D.2764>:
  node44 = malloc (16);
  node44->p = 5;
  node44->j = 10;
  kk = malloc (4);
  kk = &j;
  point = kk;
  D.2765 = *point;
  if (D.2765 != 5) goto <D.2766>; else goto <D.2767>;
  <D.2766>:
  __builtin_putchar (10);
  <D.2767>:
  noteasy = 5.77999986708164215087890625e-2;
  j = 5.0e+0;
  haha = 1.0e+1;
  noha = 5.00000007450580596923828125e-2;
  pp = 9;
  poi = 3;
  pio = 106;
  if (k == 4) goto <D.2768>; else goto <D.2769>;
  <D.2768>:
  __builtin_putchar (10);
  <D.2769>:
  j.8 = j;
  D.2771 = add (i, j.8);
  val = sub (D.2771, val);
  goto <D.2736>;
  <D.2735>:
  switch (val) <default: <D.2734>, case 3: <D.2731>, case 8: <D.2733>>
  <D.2731>:
  i = j;
  j = 2;
  goto <D.2732>;
  <D.2733>:
  i = i + 1;
  j = 6;
  goto <D.2732>;
  <D.2734>:
  i = 0;
  <D.2732>:
  i = -2;
  <D.2736>:
  if (i > 0) goto <D.2735>; else goto <D.2737>;
  <D.2737>:
  j.9 = j;
  printf ("%d\n", j.9);
  D.2773 = 0;
  goto <D.2775>;
  <D.2775>:
  j = {CLOBBER};
  a = {CLOBBER};
  goto <D.2774>;
  <D.2774>:
  return D.2773;
}

