grammar paec;

/*
 *  Plaine and Easie notation grammar.
 *  First published:  David Rizo, drizo@dlsi.ua.es, May, 21st, 2013
 *  Additional updates: Andrew Hankinson, andrew.hankinson@rism.digital, 2021—
 *
**/

incipit
    :
    clef
    (keyortimesignature)*   // order of key and time signature is not strictly enforced...
    separator
    musicalcontent
    ;


keyortimesignature
    :
    keysignature
    |
    timesignature
    ;


clef
    :
    PERCENT clefshape (MINUS | PLUS) DIGIT
    ;


keysignature
    :
    DOLLAR
    (
    (SHARP | FLAT)
    ( notename+ | squarebracket | (notename+ squarebracket)+ notename* | (squarebracket notename+)+ squarebracket? )
    )
    ;


squarebracket
    :
    (LEFTBRACKET notename+ RIGHTBRACKET)
    ;


timesignature
    :
    AT meter
    (SPACE meter)*
    ;


meter
    :
    ( ( LETTER_c | LETTER_o ) ( DOT | SLASH)? fraction? )
    |
    fraction
    ;


fraction
    :
    number (SLASH number)?
    ;


gracenote
    :
    //'g' note
    LETTER_g notepropschange* note
    |
    //'q' rhythmicvalue note
    LETTER_q notepropschange* note
    // rism nuevo Sometimes the rhythmicvalue is not given
    |
    //'qq' rhythmicvalue? note+ 'r'
    LETTER_q LETTER_q items LETTER_r
    ;


octave
    :
    OCTAVE7 | OCTAVE6 | OCTAVE5 | OCTAVE4 | OCTAVE3 | OCTAVE2 | OCTAVE1
    ;


rhythmicvalue
    :
    figure DOT*
    ;


figure
    :
    DIGIT
    ;


accidental
    :
    SHARP | DOUBLESHARP | FLAT | DOUBLEFLAT | NATURAL
    ;


musicalcontent
    :
    bar (barlines bar)* barlines?
    ;

bar
    :
    items
    |
    MEASUREREPEAT // measure repeat
    |
    MEASUREREST number? // number of repeats - in PAE the number is mandatory, but RISM contains some examples without it
    ;

items
    :
    item+
    ;


clefkeytimechange
    :
    (clef | timesignature | keysignature )+ SPACE*
    ;

item
    :
    clefkeytimechange // key, clef, time? change (it can be in the middle of a bar)
    |
    irregulargroup
    |
    triplet
    |
    notes
    |
    repeatgroup
    |
    notepropschange
    ;


repeatgroup
    :
    REPEATGRPDELIM
    items
    REPEATGRPDELIM LETTER_f+    // first a set of elements is marked, then it is repeated several times
    ;

triplet:
    LEFTPAR LEFTCURBRACES? octave? rhythmicvalue ( (notepropschange* note)+ | rest+ ) RIGHTCURBRACES? RIGHTPAR
;


// After '(' there must be the rhythmic value of the first note, even if it is equal to that of the group;
// In the example it appears 4('6DEFGA;5), the octave before the rhythm
irregulargroup:
    // rism, sometimes the figure with the total value of the group is omitted
    figure? LEFTPAR items SEMICOLON number RIGHTPAR
;



notepropschange
    :
    octave
    |
    rhythmicvalue
    |
    accidental
    ;


notes
    :
    note (CHORD notepropschange* note)*
    |
    rest
    |
    beaming
    ;


beaming
    :
    LEFTCURBRACES items RIGHTCURBRACES
    ;


note
    :
    gracenote
    |
    notevalue
    |
    notefermata
    ;


notefermata
    :
    LEFTPAR notevalue RIGHTPAR
    ;


rest
    :
    restvalue
    |
    restfermata
    ;


restfermata
    :
    LEFTPAR restvalue RIGHTPAR
    ;


notevalue
    :
    notename notesuffix? DOT* // rism contains some . following notes
    ;


restvalue
    :
    MINUS   // measure rests are outside this definition
    ;


notesuffix:
    TRILL slur? // + = slur
    |
    slur TRILL?
    ;


slur
    :
    PLUS
    ;


barlines
    :
    singlebarline
    |
    doublebarline
    |
    rightrptbarline     // double bar STAFFLINE with repeat sign on the right
    |
    leftrptbarline      //double bar STAFFLINE with repeat sign on the left
    |
    doublerptbarline    //double bar STAFFLINE with repeat sign on the left and on the right
    ;


singlebarline
    :
    (SLASH)
    ;


doublebarline
    :
    (SLASH SLASH)
    ;


rightrptbarline
    :
    (SLASH SLASH COLON)
    ;


leftrptbarline
    :
    (COLON SLASH SLASH)
    ;


doublerptbarline
    :
    (COLON SLASH SLASH COLON)
    ;


clefshape
    :
    ( LETTER_g | LETTER_G | LETTER_C | LETTER_F )
    ; // check semantically it is g, G, C, or F


notename
    :
    ( LETTER_A | LETTER_B | LETTER_C | LETTER_D | LETTER_E | LETTER_F | LETTER_G )
    ;


number
    :
    DIGIT+
    ;


separator
    :
    (SPACE | QUESTIONMARK | SEMICOLON)+
    ;


DIGIT   :   ('0'..'9');
OCTAVE7 :   APOSTROPHE APOSTROPHE APOSTROPHE APOSTROPHE;
OCTAVE6 :   APOSTROPHE APOSTROPHE APOSTROPHE;
OCTAVE5 :   APOSTROPHE APOSTROPHE;
OCTAVE4 :   APOSTROPHE;

OCTAVE1 :   COMMA COMMA COMMA;
OCTAVE2 :   COMMA COMMA;
OCTAVE3 :   COMMA;


// letters (sorted lexigraphically) and following precedence
DOUBLEFLAT      :   'bb';
FLAT            :   'b';
LETTER_A        :   'A';
LETTER_B        :   'B';
LETTER_c        :   'c';
LETTER_C        :   'C';
LETTER_D        :   'D';
LETTER_E        :   'E';
LETTER_f        :   'f';
LETTER_F        :   'F';
LETTER_g        :   'g';
LETTER_G        :   'G';
MEASUREREPEAT   :   'i';
NATURAL         :   'n';
LETTER_o         :   'o';
LETTER_q        :   'q';
LETTER_r        :   'r';
TRILL           :   't';

DOUBLESHARP     :   'xx';
SHARP           :   'x';

PERCENT         :   '%';
MINUS           :   '-';
PLUS            :   '+';
DOLLAR          :   '$';
LEFTBRACKET     :   '[';
RIGHTBRACKET    :   ']';
AT              :   '@';
SPACE           :   ' ';

CHORD           :   '^';
TAB             :   '\t';
MEASUREREST     :   '=';
LEFTPAR         :   '(';
RIGHTPAR        :   ')';
LEFTCURBRACES   :   '{';
RIGHTCURBRACES  :   '}';
SEMICOLON       :   ';';
REPEATGRPDELIM  :   '!';
SLASH           :   '/';
fragment
APOSTROPHE      :   '\'';
fragment
COMMA           :   ',';
COLON           :   ':';
QUESTIONMARK    :   '?';
DOT             :   '.';

EOL             :   ('\n'|'\r') -> skip;

UNKNOWN_CHAR    : . ;
