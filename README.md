#   g s _ c i t e d _ a r t i c a l _ c r a w l e r  
  
 # #   O v e r v i e w  
  
 T h i s   P y t h o n - b a s e d   w e b   s c r a p e r   i s   d e s i g n e d   t o   r e t r i e v e   c i t a t i o n   i n f o r m a t i o n   f r o m   G o o g l e   S c h o l a r   f o r   a   s p e c i f i e d   a r t i c l e .   I t   e x t r a c t s   d e t a i l s   s u c h   a s   t h e   t i t l e ,   a u t h o r s ,   p u b l i c a t i o n   p l a t f o r m ,   a n d   y e a r   o f   a l l   c i t i n g   d o c u m e n t s .  
  
 # #   F e a t u r e s  
  
 -   * * F e t c h   C i t a t i o n   D e t a i l s : * *   A u t o m a t i c a l l y   g a t h e r s   c o m p r e h e n s i v e   c i t a t i o n   d a t a   f r o m   G o o g l e   S c h o l a r .  
 -   * * E a s y   t o   U s e : * *   U s e r - f r i e n d l y   c o m m a n d   l i n e   i n t e r f a c e .  
 -   * * O u t p u t   F o r m a t t i n g : * *   O r g a n i z e s   c i t a t i o n   i n f o r m a t i o n   i n   a   s t r u c t u r e d   f o r m a t   f o r   e a s y   a n a l y s i s .  
  
 # #   R e q u i r e m e n t s  
  
 -   P y t h o n   3 . 6   o r   h i g h e r  
 -   P l a t f o r m : W i n d o w s  
 -   [ c h r o m e d r i v e r ] ( h t t p s : / / c h r o m e d r i v e r . c h r o m i u m . o r g / d o w n l o a d s )  
 -   G o o g l e   C h r o m e  
  
 # #   I n s t a l l a t i o n  
  
 C l o n e   t h e   r e p o s i t o r y   t o   y o u r   l o c a l   m a c h i n e :  
  
 ` ` ` b a s h  
 g i t   c l o n e   g i t @ g i t h u b . c o m : s h o w l i b i a / g s _ c i t e d _ a r t i c a l _ c r a w l e r . g i t  
 c d   g s _ c i t e d _ a r t i c a l _ c r a w l e r  
 ` ` `  
  
 I n s t a l l   t h e   r e q u i r e d   P y t h o n   l i b r a r i e s :  
  
 ` ` ` b a s h  
 p i p   i n s t a l l   - r   r e q u i r e m e n t s . t x t  
  
 ` ` `  
  
 # #   U s a g e  
  
 R u n   t h e   s c r a p e r   u s i n g   t h e   f o l l o w i n g   c o m m a n d :  
  
 ` ` ` b a s h  
 p y t h o n   c r a w l e r . p y   " a r t i c a l n a m e "  
 ` ` `  
  
 # #   O u t p u t  
  
 T h e   s c r i p t   w i l l   o u t p u t   a   C S V   f i l e   n a m e d   ` c i t e d _ a r t i c l e s . j s o n `   c o n t a i n i n g   t h e   f o l l o w i n g   c o l u m n s :  
  
 -   * * T i t l e : * *   T i t l e   o f   t h e   c i t i n g   a r t i c l e .  
 -   * * C i t a t i o n * * : G B / T   7 7 1 4   c i t a t i o n   t e x t  
 -   * * A u t h o r s : * *   L i s t   o f   a u t h o r s .  
 -   * * P u b l i c a t i o n : * *   P l a t f o r m   o r   j o u r n a l   w h e r e   t h e   a r t i c l e   i s   p u b l i s h e d .  
 -   * * Y e a r : * *   P u b l i c a t i o n   y e a r 