;Header and description

(define (domain Smartroom)

;remove requirements that are not needed
(:requirements :strips :typing :negative-preconditions )

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
light blind heater cooler - object
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
(lState ?l - light)
(bState ?b - blind)
(hState ?h - heater)
(cState ?c - cooler)
)
;define actions here

(:action LightSwitchON
:parameters (?x - light)
:precondition (not (lState ?x))
:effect (lState ?x)
)
    
(:action LightSwitchOFF
:parameters (?x - light)
:precondition (lState ?x)
:effect (not (lState ?x))
)

(:action closeBlind
:parameters (?x - blind)
:precondition (bState ?x)
:effect (not (bState ?x))
)

(:action openBlind
:parameters (?x - blind)
:precondition (not (bState ?x))
:effect (bState ?x)
)

(:action HeaterSwitchON
:parameters (?x - heater)
:precondition (not (hState ?x))
:effect (hState ?x)
)

(:action HeaterSwitchOFF
:parameters (?x - heater)
:precondition (hState ?x)
:effect (not (hState ?x))
)

(:action CoolerSwitchON
:parameters (?x - cooler)
:precondition (not (cState ?x))
:effect (cState ?x)
)

(:action CoolerSwitchOFF
:parameters (?x - cooler)
:precondition (cState ?x)
:effect (not (cState ?x))
)

)
