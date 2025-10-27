% ==========================================
% COCKTAIL EXPERT SYSTEM - GUI VERSION
% (packaged copy)
% ==========================================

:- dynamic known/3.

% Cocktail database
cocktail(mojito, rum, 
    [white_rum, mint, lime, sugar, soda_water],
    [muddling, shaking], 
    [refreshing, minty, sweet, citrus], 
    medium, beginner, summer, [party, casual], highball, 
    'Cuban origin, named after mojo sauce').

cocktail(daiquiri, rum,
    [white_rum, lime, simple_syrup],
    [shaking, straining],
    [sour, sweet, strong, citrus],
    strong, beginner, summer, [party, celebration], cocktail,
    'Invented by American miners in Cuba').

cocktail(negroni, gin,
    [gin, campari, sweet_vermouth],
    [stirring, straining],
    [bitter, herbal, strong, complex],
    strong, intermediate, all_seasons, [aperitif, sophisticated], rocks,
    'Italian cocktail named after Count Negroni').

cocktail(aviation, gin,
    [gin, maraschino, violet_liqueur, lemon],
    [shaking, straining],
    [floral, citrus, complex, balanced],
    medium, expert, spring, [romantic, sophisticated], cocktail,
    'Pre-prohibition classic with floral notes').

cocktail(espresso_martini, vodka,
    [vodka, coffee_liqueur, fresh_espresso, simple_syrup],
    [shaking, straining],
    [bitter, sweet, creamy, caffeinated],
    medium, intermediate, all_seasons, [after_dinner, party], martini,
    'Created for a supermodel who wanted something to wake her up').

cocktail(white_russian, vodka,
    [vodka, coffee_liqueur, heavy_cream],
    [building, layering],
    [creamy, sweet, rich, coffee],
    medium, beginner, winter, [after_dinner, relaxing], rocks,
    'Gained popularity from The Big Lebowski').

cocktail(old_fashioned, whiskey,
    [bourbon, sugar, bitters, orange, cherry],
    [muddling, stirring],
    [strong, sweet, aromatic, bitter],
    strong, intermediate, winter, [sophisticated, relaxing], rocks,
    'One of the oldest known cocktail recipes').

cocktail(whiskey_sour, whiskey,
    [bourbon, lemon, simple_syrup, egg_white],
    [dry_shaking, shaking],
    [sour, sweet, creamy, balanced],
    medium, intermediate, all_seasons, [casual, party], rocks,
    'Classic sour dating back to 1870s').

cocktail(paloma, tequila,
    [tequila, grapefruit_soda, lime, salt],
    [building, stirring],
    [refreshing, bitter, citrus, salty],
    medium, beginner, summer, [casual, party], highball,
    'Most popular tequila cocktail in Mexico').

% ========== GUI COMPATIBLE FUNCTIONS ==========

find_and_display_recommendations :-
    findall(Cocktail-Score, (
        cocktail(Cocktail, BaseSpirit, Ingredients, Techniques, Flavors, Strength, Complexity, Season, Occasion, Glass, History),
        calculate_match_score(Cocktail, Score),
        Score >= 3
    ), Candidates),
    
    (   Candidates = []
    ->  write('No strong matches found with your preferences.'), nl
    ;   sort_candidates(Candidates, Sorted),
        show_scored_recommendations(Sorted)
    ).

browse_all_cocktails :-
    findall(Cocktail, cocktail(Cocktail, BaseSpirit, Ingredients, Techniques, Flavors, Strength, Complexity, Season, Occasion, Glass, History), Cocktails),
    display_cocktail_list(Cocktails).

% ========== MATCHING ENGINE ==========

calculate_match_score(Cocktail, TotalScore) :-
    cocktail(Cocktail, BaseSpirit, _Ingredients, _Techniques, Flavors, StrengthLevel, ComplexityLevel, Season, Occasion, _Glass, _History),
    
    BaseScore = 0,
    
    % Spirit preference (HIGH PRIORITY - 3 points)
    (   known(spirit_preference, BaseSpirit, _) 
    ->  SpiritScore = 3 
    ;   known(spirit_preference, no_preference, _)
    ->  SpiritScore = 1
    ;   SpiritScore = 0
    ),
    
    % Strength matching (MEDIUM PRIORITY - 2 points)
    (   known(strength, UserStrength, _),
        strength_value(StrengthLevel, CocktailStrength),
        abs(UserStrength - CocktailStrength) =< 2
    ->  StrengthScore = 2
    ;   StrengthScore = 0
    ),
    
    % Skill level matching (HIGH PRIORITY - 3 points)
    (   known(skill_level, UserSkill, _),
        complexity_value(ComplexityLevel, CocktailComplexity),
        skill_sufficient(UserSkill, CocktailComplexity)
    ->  SkillScore = 3
    ;   SkillScore = 0
    ),
    
    % Season matching (MEDIUM PRIORITY - 2 points)
    (   known(current_season, CurrentSeason, _),
        (   Season == all_seasons 
        ;   Season == CurrentSeason 
        )
    ->  SeasonScore = 2
    ;   SeasonScore = 0
    ),
    
    % Occasion matching (MEDIUM PRIORITY - 2 points)
    (   known(occasion_type, OccasionType, _),
        member(OccasionType, Occasion)
    ->  OccasionScore = 2
    ;   OccasionScore = 0
    ),
    
    % Flavor notes matching (LOW PRIORITY - 1 point)
    (   known(flavor_notes, UserFlavor, _),
        member(UserFlavor, Flavors)
    ->  FlavorScore = 1
    ;   FlavorScore = 0
    ),
    
    TotalScore is BaseScore + SpiritScore + StrengthScore + SkillScore + SeasonScore + OccasionScore + FlavorScore.

% ========== DISPLAY FUNCTIONS ==========

show_scored_recommendations([]).
show_scored_recommendations([Cocktail-Score|Rest]) :-
    cocktail(Cocktail, BaseSpirit, Ingredients, Techniques, Flavors, Strength, Complexity, Season, Occasion, Glass, History),
    
    format('Match Score: ~w/13~n', [Score]),
    format('**~w**~n', [Cocktail]),
    format('Base Spirit: ~w~n', [BaseSpirit]),
    format('Strength: ~w | Complexity: ~w~n', [Strength, Complexity]),
    format('Ingredients: ', []), write_list(Ingredients), nl,
    format('Techniques: ', []), write_list(Techniques), nl,
    format('Flavors: ', []), write_list(Flavors), nl,
    format('Best for: ', []), write_list(Occasion), nl,
    format('Season: ~w | Glass: ~w~n', [Season, Glass]),
    format('History: ~w~n', [History]),
    format('----------------------------------------~n', []),
    show_scored_recommendations(Rest).

display_cocktail_list([]).
display_cocktail_list([Cocktail|Rest]) :-
    cocktail(Cocktail, BaseSpirit, Ingredients, Techniques, Flavors, Strength, Complexity, Season, Occasion, Glass, History),
    format('**~w**~n', [Cocktail]),
    format('Spirit: ~w | Strength: ~w | Skill: ~w~n', [BaseSpirit, Strength, Complexity]),
    format('Flavors: ', []), write_list(Flavors), nl,
    format('Best for: ', []), write_list(Occasion), nl,
    format('----------------------------------------~n', []),
    display_cocktail_list(Rest).

% ========== UTILITY FUNCTIONS ==========

strength_value(light, 3).
strength_value(medium, 6).
strength_value(strong, 9).

complexity_value(beginner, 1).
complexity_value(intermediate, 2).
complexity_value(expert, 3).

skill_sufficient(expert, _).
skill_sufficient(intermediate, Complexity) :- Complexity =< 2.
skill_sufficient(beginner, Complexity) :- Complexity =< 1.

write_list([]) :- write('').
write_list([X]) :- format('~w', [X]).
write_list([X|Rest]) :-
    format('~w', [X]),
    (   Rest \= []
    ->  write(', '),
        write_list(Rest)
    ;   true
    ).

sort_candidates(Candidates, Sorted) :-
    predsort(compare_scores, Candidates, Reversed),
    reverse(Reversed, Sorted).

compare_scores(Order, _-Score1, _-Score2) :-
    compare(Order, Score1, Score2).

% ========== INITIALIZATION ==========

% Initialize with some default knowledge if needed
:- initialization(main).

main :-
    write('Cocktail Expert System loaded successfully.'), nl.
