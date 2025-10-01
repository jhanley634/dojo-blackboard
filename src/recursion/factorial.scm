#! /usr/bin/env racket

#lang racket


(+ 1 2 3)


(define (fact-slow n)  ; TCO is disabled, so the call stack grows
  (if (zero? n)
      1
      (* n (fact-slow (sub1 n)))))


(fact-slow 5)
(fact-slow 100)



(define (fact n)
  (_fact n 1))

(define (_fact n acc)
  (if (zero? n)
      acc
      (_fact (sub1 n) (* acc n))))

(fact 5)
(fact 100)


(define (measure-time f . args)
  (define start-time (current-inexact-milliseconds))
  (define result (apply f args))
  (define end-time (current-inexact-milliseconds))
  (values result (inexact->exact (round (- end-time start-time)))))

(let ([n 250000])
  (for ([fn (in-list (list fact-slow fact))])
    (let-values ([(result elapsed-time) (measure-time fn n)])
      (printf "Factorial ~a found by ~a~ in ~a msec\n"
              n fn elapsed-time))))
