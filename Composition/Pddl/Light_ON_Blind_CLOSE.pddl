(define (problem ligting3) (:domain Smartroom)
(:objects 
l - light
b - blind
h - heater
c - cooler
)

(:init
    ;todo: put the initial state's facts and numeric values here
    <Placeholder>
)

(:goal (and
    ;todo: put the goal condition here
    (lState l)
    (not (bState b))
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
