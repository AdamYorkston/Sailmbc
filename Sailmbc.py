from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import time
import datetime as dt
import os
import pickle
import base64
import random


class Racer:
    ''' A Racer is a unique competitor in a race'''

    def __init__(self):
        self.helm_name = tk.StringVar()
        self.sail_number = tk.StringVar()
        self.boat_class = 'N/A'
        self.handicap = 1000
        self.finish_time = tk.StringVar()
        self.rank = tk.StringVar()


class MainApplication:
    ''' An instance of the main SAILMBC program '''

    def __init__(self, master):
        self.master = master  # master is generally the TK window
        self.starters = []  # competitors in the race
        self.Handicaps = {  # PY handicap values for common boats
            "BOD": 1142,
            "Comet": 1207,
            "K1": 1070,
            "Laser": 1099,
            "Laser 4.7": 1207,
            "Laser Radial": 1145,
            "Mirror (Single)": 1380,
            "Mirror (Double)": 1390,
            "National 12 (Julian)": 1089,
            "OK": 1104,
            "Optimist": 1642,
            "Oulton Rater XX2": 980,
            "Phantom": 1002,
            "RS 300": 970,
            "RS Aero 5": 1136,
            "RS Aero 7": 1065,
            "RS Aero 9": 1014,
            "RS Tera Pro": 1359,
            "RS Tera Sport": 1438,
            "RS Vareo": 1093,
            "Solo": 1143,
            "Splash": 1220,
            "Squib": 1142,
            "Streaker": 1128,
            "Topper": 1363,
            "Wanderer (Spinnaker)": 1190,
            "Wanderer (No Spinnaker)": 1204,
            "Waveney One Design": 1142,
            "Wayfarer": 1102,
            "Yare & Bure": 1142}
        # Quotes used in the 'About Sailmbc' page
        self.quotes = ["'It's really cool!!!' - Bethany",
                       "'This is the highlight of my life' - Ian Colby (probably)",
                       "'There are apps that do that already' - Jordan (there aren't)",
                       "'What's a Sailmbc?' - Tom Betts",
                       " 'It's pretty clever'- Jamie",
                       "'The greatest thing since I beat Harry in a wanderer' - Kyle",
                       "'Is that a potato?!' - Harry",
                       "'Brum brum brrrum brum brum' - LOBMBC"]
        self.comments = []  # User inputed comments about the race
        # The program icon image
        icon = """
        AAABAAMAEBAAAAEAIABoBAAANgAAACAgAAABACAAKBEAAJ4EAAAwMAAAAQAgAGgmAADGFQAAKAAA
        ABAAAAAgAAAAAQAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4eIUQcHB9I
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAe
        HiB2HBwcGwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAHR0hkQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAB0dIZEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAB4eHhFxcXLW9/f3o/Hx8V3S0tIRAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeHh5Cnp6fyP7+/v/+/v7/+/v79vLy9I3GxsYJAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHh4gddDQ0qv+/v7//v7+//7+/v/+/v7/+Pj4
        z8SqiScAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0dIZHgz7nA59O9/+7h0v/+/v7/
        /v7+//7+/v+sZxv8oVQCscKcc13c3Nwlf39/AgAAAAAAAAAAAAAAAAAAAAAgHiCVoVQB8qRWAP+k
        VQD/wY5V//n18P/17OP/o1YA/6RVAP/hya7//v7+//n5+eny8vKS3d3dHgAAAAAfHx8QOiocraNV
        AP+jVQD/o1UA/6NWAP+vayH/sY6L/4lIKf+gVAX/69vJ/+vax//p18T/9/Hq//v7+/YAAAAAGxsf
        QWQ/F7HEk1z/3L6e/8OQWf+lWAP/pFUA/0Eil/8AAP7/GQ3W/6RWAP+jVgD/o1UA/6RXA/+5fj3/
        AAAAABwcIHTOy8q0/v7+//7+/v/+/v7/7uHS/8SRWf8yHbj/AAD+/zIasP+ycCj/yZto/8qebP+/
        iU3/q2QW/wAAAAAdHSGR9vb2zf7+/v/+/v7//v7+//7+/v/+/v3/qmMV/5VOFf+zj4j//v79//7+
        /v/+/v7//v7+//38+/8AAAAAJSUpm/r6+vn+/v7//v7+//7+/v/+/v7/8+ne/6NVAP+jVQD/3cKj
        //f398rx8fFy6OjoOMjIyBzFxcUWHh4eEVVVWLj29vaP8PDwbfDw8Fjw8PBV8PDwadrCqJSjVAC3
        oVMAhsmriTQAAAAAAAAAAAAAAAAAAAAAAAAAAB4eILsdHSHHAAAAAQAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAACAAAABAAAAAAQAg
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeHiBt
        HBwhnwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAB0dIaIdHSGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHh4g1B0dIE8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABMTEw0dHSD5GhoaHQAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        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
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAHR0gVh4eIMsdHSH3Hh4gwwAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAADAAAABgAAAA
        AQAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAABHR0hpR0dIcYdHR0rAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASEhIOHh4h0B0dId0bGxscAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAdHR0r
        Hh4h4h4eIsIAADMFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAeHiFMHR0h7h0dH5EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEeHiBuHh4g+RwcH1kAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACoq
        KgYeHh+QHh4h/B0dHSMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAB4eHhEeHiCyHx8h5QAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABsbJBweHiDUHh4hrwAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAB0dIyseHiHyHR0gdwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4eIVQeHiH7Hh4hRAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0dIIwdHSHnGxsi
        JQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAABwcIMMdHSHIHx8fGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFRUVDB4eIPAlJSivtbW1U9XV1THg4OAZqampCQAA
        AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwhNh4eIf1l
        ZWbT9PT08Pf3+PDy8vLI7u7umeXl5W3R0dE+o6OjDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAHBwgbR4eIfaOjo/c+/v7/P7+/v/+/v7//f39/vr6+vj5+fnp8fHxz9zc3IW3
        t7crf39/AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABHR0gpR4eIOugoKG6+vr6/P7+/v/+/v7/
        /v7+//7+/v/+/v7//v7+//7+/v/39/f15OTkr87Ozj/X19cNAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVFRUMHh4h
        zx8fId64uLmQ+fn5+v7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//f3+PDr6+uf
        yMjIMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAaGiAnHR0g4R0dIcjc3Nx2+vr6+f/////+/v7///////7+/v//////////
        //7+/v/+/v7//v7+//7+/v/8/P389fX14dDQ0GJ/f38EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAbGyJKHh4h7R8fIprr6+uF/f39/f//
        /////////v7+//7+/v///////v7+//7+/v/+/v7//v7+//7+/v/+/v7///////r6+/bi4uKFycnJ
        EwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAc
        HCFrHR0g+CkpLmjt7e2d/v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+///////+/v7//v7+//7+
        /v/+/v7//v7+///////6+vr47OzsqcbGxi0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAACoqKgYcHCCNHh4h/FVVWTzu7u65//////7+/v/+/v7//v7+//7+/v/+
        /v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+///////+/v7//Pz8/uXXxtmVXiJvbUg2DgAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8fHxAeHiGvHh4h58bGxiTx8fLc
        /v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+///////+/v7//v7+///////+
        /v7//v7+/9azjf+jVgH/nloQ3pNYGXCQUg0lf1UVDAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        ABwcHBsdHSHQHR0gtNDQ0Df49/f2/v38//z7+v/8+vf/+vbx//37+f/+/v3//v7+////////////
        //////7+/v/+/v7//v7+//7+/v/+/v7//v7+/8GNU/+kVgD/pFYA/6NVAP2eVQTemlIEo5hVDmur
        iGU6n5+fEAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4eJCodHSHvHBwgfZxrNWi8hUj/u4FB/7h8Of+2dzL/snEp
        /7h7OP/Eklz/59O+//7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v///////f37/69pHv+kVgD/
        pFUA/6RVAP+kVQD/pFYA/6VbC/fXuZno8vLy1Obm5q/c3Nx8v7/CSH9/fxIAAAABAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwcI1AeHiH8HBwgR5RS
        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
        Hh4g7CEhI6DSwKuK9vHr/v/////+/v7//v7+//7+/v/+/v7//v7+//7+/v///////v7+//n07//Q
        qX3/r2of/6VYA/+kVgD/pFYA/4tJJf8NB+n/AAD//wAA//8AAP7/AAD+/wAA/v8EAvf/gUM1/6RW
        AP+jVgD/pFYA/6RWAP+kVgD/pFYA/6RWAP+kVgD/pFYA/6RWAP+kVgD/pFYA/6RWAP+jVgD/pFYA
        /wAAAAAAAAAAAAAAAAAAAAAdHR9oHR0h9zU1N3Pu7u6u/v7+///////+/v7///////7+/v//////
        /////////////////v7+///////+/fz/7NzL/8+nev+2eDT/plkF/3lAQP8CAfr/AAD+/wAA/v8A
        AP7/AAD+/wAA//8SCeL/jUoi/6RWAP+kVgD/qWAQ/7h8Of/BjVP/yJpm/8maZ//Ek1z/vodJ/7Z5
        Nf+uaR3/plsH/6RWAP+kVgD/pFYA/wAAAAAAAAAAAAAAADMzMwUdHSGKHh4h/WhoaEfy8vLR/v7+
        //7+/v///////v7+/////////////v7+//7+/v/+/v7//v7+///////+/v7//v7+//37+v/17eT/
        4smv/5RpcP8xGbH/Ewng/wIB+/8AAP7/AAD//wAA/v8kE8X/lU4X/7BuJf/SrYT/7d7P//bu5//5
        9O///Pn2//z59//69vL/+PPt//Xu5f/y6N3/69rI/9i3kv+7gUL/plsI/wAAAAAAAAAAAAAAACIi
        Ig8dHSKsHh4h67u7uzX09PTx/v7+//7+/v/+/v7//v7+//7+/v////////////7+/v///////v7+
        ///////+/v7//v7+///////+/v7//////9CofP+jVQD/olQC/5ROGP93PkX/Vy52/zgepf9aPqT/
        1Lqp//z6+P/+/v7////////////+/v7//v7+///////+/v7//v7+//7+/v/+/v7///////7+/v/+
        /v7/9e3j/wAAAAAAAAAAAAAAAB0dHRodHSHNHh4gutPT01j7+/v+/v7+//7+/v/+/v7//v7+//7+
        /v/+/v7//v7+///////+/v7//v7+//7+/v/+/v7//v7+//7+/v/+/v7//v7+/7uBQv+jVgD/o1UA
        /6NWAP+kVgD/o1UA/6NWAf/GmGn/+/j2//7+/v/+/v7//v7+///////+/v7//v7+//7+/v/+/v7/
        //////7+/v/+/v7//v7+//7+/v/+/v7//v7+/wAAAAAAAAAAAAAAABkZHygeHiHtHR0fgd/f35H+
        /v7//v7+///////+/v7//////////////////v7+//7+/v/////////////////+/v7/////////
        /////////Pr3/6lgEP+jVgD/pFYA/6NWAP+jVgD/o1UA/6VYBP/Ur4f//f39//7+/v///////v7+
        //7+/v/+/v7//v7+//7+/v/+/v7//v7+//7+/v///////v7+//7+/v///////v7+/wAAAAAAAAAA
        AAAAABsbIkseHiH8HR0hTefn6M3//////v7+//7+/v/+/v7//v7+///////+/v7//v7+//7+/v/+
        /v7//v7+//7+/v///////v7+//7+/v//////7d7N/6RWAf+jVQD/o1UA/6NWAP+jVQD/pFYA/6hf
        Dv/fxaj///////7+/v/+/v7//v7+//z8/P76+vr1+fn65/X19dfo6Oi13t7gjNXV1W/Ozs5ZxsbG
        Tb29vUbHx8dJyMjMUAAAAAAAAAAAAAAAAB0dIYIeHiHsPj5CPfT09fX//////v7+//7+/v/+/v7/
        /v7+//7+/v/+/v7//v7+//7+/v/+/v7////////////+/v7//v7+//7+/v/+/v7/2LeU/6NWAP+j
        VgD/o1YA/6NVAP+kVgD/o1YA/6xmGf/r28n//v7+//7+/v/5+fn38fHxzurq6pXl5eVjzMzMOJOT
        oRNVVVUDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4eILodHSHOmZmZ
        Z/39/f/+/v7//v7+//7+/v/+/v7///////7+/v/+/v7///////7+/v/+/v7//v7+///////+/v7/
        /v7+//7+/v/+/v7/xJJb/6NVAP+jVQD/o1YA/6NVAP+jVgD/o1UA/7FvJf/27+f//Pz8/ujo6MrY
        2NhV0dHRHL+/vwgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAkBx4eIeokJCe02traxf7+/v/+/v7/+/v7/vr6+vn6+vry+vr67Pr6+uf5+fnl+vr6
        4vn5+eH5+fni+vr65Pr6+uj6+vrv+vr6+Pv7+/769/P/tHUv/6NVAP+jVQD/o1YA/6NWAP+jVAD9
        o1UA8rN3NeDl5eSqwcHBRlVVVQMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGxshLh4eIfxLS03B5eXlye/v77ru7u6e6Ojqh+Xl
        5W/f399a29vbSNLS0jnFxcoxwsLCKru7uybAwMApycnPMNTU1Dzb29tQ5eXlbOjo6Irk29Crp2gh
        xqNUAOSjVQD3o1UA5aNUALujVgCOpVQAW6VfEyhmZmYFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEXFxcLHh4hbB4eIvcv
        LzJ12traHMzMzBSysrIKf39/BAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAH9/fwS7qpkPlF8fGKJVACSjUQAyolUAJKVZABSqVQAGAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAB0dIJUeHiLvHh4h/R4eIfkeHiGfGhohJgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0dIKMeHiH7Hx8i/x4eIv8eHiL/Hh4hwAAAAAYAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABgYJBUdHSBvHh4h
        uB0dIe8eHiHkHh4gfwAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAA==
        """
        icondata = base64.b64decode(icon)
        tempFile = "SMBCicon.ico"  # store the icon as a temporary file
        iconfile = open(tempFile, "wb")
        iconfile.write(icondata)
        iconfile.close()
        master.wm_iconbitmap(tempFile)  # set the icon
        time.sleep(0.1)  # ensure the file isn't deleted prematurely
        os.remove(tempFile)

        self.date = dt.datetime.now().date()
        # StringVar is needed to set/update text in widget
        self.date_text = tk.StringVar()  
        self.date_text.set(str(self.date))

        self.time_start = dt.datetime.now().time().replace(microsecond=0,
                                                           second=0)
        self.time_start_text = tk.StringVar()
        self.time_start_text.set(str(self.time_start))

        self.current_time_text = tk.StringVar()
        self.time_elapsed_text = tk.StringVar()
        self.elapsed_or_until_start = tk.StringVar()
        self.race_title_text = tk.StringVar()
        self.set_title()

        master.geometry('850x650')  # window size
        self.bg_colour = "#a1dbcd"  # background colour
        master.configure(background=self.bg_colour)

        master.bind('<Control-s>', lambda x: self.save())  # bind quicksave

        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New File", command=new_window)
        filemenu.add_command(label="Open File", command=lambda: self.load())
        filemenu.add_command(label="Open File in New Window",
                             command=lambda: load_in_new_window())
        filemenu.add_separator()
        filemenu.add_command(label="Save", command=lambda: self.save())
        filemenu.add_command(label="Save As", command=lambda: self.save_as())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=on_closing(self.master))
        menubar.add_cascade(label="File", menu=filemenu)
        addmenu = tk.Menu(menubar, tearoff=0)
        for i in range(len(self.Handicaps)):
            addmenu.add_command(
                label=list(self.Handicaps.keys())[i],
                command=self.add_starter(list(self.Handicaps.keys())[i]))
        menubar.add_cascade(label="Add Starter", menu=addmenu)
        menubar.add_command(label="Sort Boats",
                            command=lambda: self.sort_starters())
        #menubar.add_command(label="About Sailmbc", command=lambda: self.display_about())
        menubar.add_command(label="Export as HTML",
                            command=self.print_sailwave)
        master.config(menu=menubar)

        self.update_display()
        master.after(1, self.timed_update())  # runs the autoupdate function

    def set_title(self):
        displayList = []
        raceTitle = self.race_title_text.get()
        if len(raceTitle) != 0:
            displayList.append(raceTitle)
        else:
            displayList.append('Sailmbc')
        try:
            displayList.append(self.master.filename)
        except Exception:
            pass
        self.master.title(' - '.join(displayList))

    def update_display(self):
        try:
            self.comments = self.comment_box.get("1.0", "end-1c")
        except Exception:
            pass
        self.clear_screen()
        self.set_title()
        self.rank_starters()

        lbl = tk.Label(self.master, text='Race Title:', bg=self.bg_colour)
        lbl.grid(column=0, row=0, sticky=tk.W)
        ety = tk.Entry(self.master,
                       textvariable=self.race_title_text, width=40)
        ety.grid(column=1, row=0, columnspan=4, sticky=tk.W)
        ety.bind('<Return>', lambda x: self.update_display())
        lbl = tk.Label(self.master, text='Date:', bg=self.bg_colour)
        lbl.grid(column=0, row=1, sticky=tk.W)
        ety = tk.Entry(self.master, textvariable=self.date_text, width=12)
        ety.grid(column=1, row=1, sticky=tk.W)
        lbl = tk.Label(self.master, text='Start Time:', bg=self.bg_colour)
        lbl.grid(column=0, row=2, sticky=tk.W)
        ety = tk.Entry(self.master,
                       textvariable=self.time_start_text, width=12)
        ety.grid(column=1, row=2, sticky=tk.W)
        ety.bind('<Return>', lambda x: self.update_display())
        lbl = tk.Label(self.master, text='Current Time:', bg=self.bg_colour)
        lbl.grid(column=0, row=3, sticky=tk.W)
        lbl = tk.Label(self.master,
                       textvariable=self.current_time_text, bg=self.bg_colour)
        lbl.grid(column=1, row=3, sticky=tk.W)
        lbl = tk.Label(self.master, textvariable=self.elapsed_or_until_start,
                       bg=self.bg_colour)
        lbl.grid(column=0, row=4, sticky=tk.W)
        lbl = tk.Label(self.master,
                       textvariable=self.time_elapsed_text, bg=self.bg_colour)
        lbl.grid(column=1, row=4, sticky=tk.W)

        lbl = tk.Label(self.master, text='Comments:', bg=self.bg_colour)
        lbl.grid(column=4, row=0, sticky=tk.W)
        self.comment_box = tk.Text(self.master, height=5, width=45)
        self.comment_box.grid(column=5,
                              row=0, rowspan=4, columnspan=30, sticky=tk.W)
        self.comment_box.insert(tk.END, self.comments)

        lbl = tk.Label(self.master, text='-'*500, bg=self.bg_colour)
        lbl.grid(column=0, row=5, sticky=tk.W, columnspan=1000)

        lbl = tk.Label(self.master, text='Class' + ' ' * 14, bg=self.bg_colour)
        lbl.grid(column=0, row=6, sticky=tk.W)
        lbl = tk.Label(self.master, text='Sail #' + ' ' * 6, bg=self.bg_colour)
        lbl.grid(column=1, row=6, sticky=tk.W)
        lbl = tk.Label(self.master,
                       text='Helm Name' + ' ' * 22, bg=self.bg_colour)
        lbl.grid(column=2, row=6, sticky=tk.W)
        lbl = tk.Label(self.master, text='PY' + ' ' * 10, bg=self.bg_colour)
        lbl.grid(column=3, row=6, sticky=tk.W)
        lbl = tk.Label(self.master,
                       text='Finish Time' + ' ' * 4, bg=self.bg_colour)
        lbl.grid(column=4, row=6, sticky=tk.W)
        lbl = tk.Label(self.master,
                       text='Elapsed Time' + ' ' * 4, bg=self.bg_colour)
        lbl.grid(column=5, row=6, sticky=tk.W)
        lbl = tk.Label(self.master,
                       text='Adjusted Time' + ' ' * 4, bg=self.bg_colour)
        lbl.grid(column=6, row=6, sticky=tk.W)
        lbl = tk.Label(self.master,
                       text='Position' + ' ' * 4, bg=self.bg_colour)
        lbl.grid(column=7, row=6, sticky=tk.W)
        lbl = tk.Label(self.master, text=' ' * 12, bg=self.bg_colour)
        lbl.grid(column=8, row=6, sticky=tk.W)
        offset = 8
        for i in range(len(self.starters)):
            lbl = tk.Label(self.master, text=self.starters[i].boat_class,
                           bg=self.bg_colour)
            lbl.grid(column=0, row=i+offset, sticky=tk.W)
            lbl = tk.Entry(self.master,
                           textvariable=self.starters[i].sail_number, width=7)
            lbl.grid(column=1, row=i+offset, sticky=tk.W)
            lbl = tk.Entry(self.master,
                           textvariable=self.starters[i].helm_name)
            lbl.grid(column=2, row=i+offset, sticky=tk.W)
            lbl = tk.Label(self.master, text=self.starters[i].handicap,
                           bg=self.bg_colour)
            lbl.grid(column=3, row=i+offset, sticky=tk.W)
            ety = tk.Entry(self.master,
                           textvariable=self.starters[i].finish_time, width=10)
            ety.grid(column=4, row=i+offset, sticky=tk.W)
            ety.bind('<Return>', lambda x: self.update_display())
            try:
                parts = self.starters[i].finish_time.get().split(':')
                if len(parts) == 1 or len(parts) > 3:
                    raise
                h = int(parts[0])
                m = int(parts[1])
                try:
                    s = int(parts[2])
                except Exception:
                    s = 0
                finish_time = dt.time(h, m, s)
                if finish_time < self.time_start:
                    raise
                time_elapsed = dt.datetime.combine(dt.date.min, finish_time) \
                    - dt.datetime.combine(dt.date.min, self.time_start)
                secs = time_elapsed.seconds
                secs_adjusted = round(secs * 1000 / self.starters[i].handicap)
                time_adjusted = dt.timedelta(seconds=secs_adjusted)
                lbl = tk.Label(self.master, text=str(time_elapsed),
                               bg=self.bg_colour)
                lbl.grid(column=5, row=i + offset, sticky=tk.W)
                lbl = tk.Label(self.master, text=str(time_adjusted),
                               bg=self.bg_colour)
                lbl.grid(column=6, row=i + offset, sticky=tk.W)
                lbl = tk.Label(self.master, textvariable=self.starters[i].rank,
                               bg=self.bg_colour)
                lbl.grid(column=7, row=i+offset, sticky=tk.W)
            except Exception:
                if self.starters[i].finish_time.get() == '':
                    pass
                else:
                    lbl = tk.Label(self.master, text=str('INVALID TIME'),
                                   bg=self.bg_colour)
                    lbl.grid(column=5, row=i+offset, sticky=tk.W)
            but = tk.Button(self.master, text='Time',
                            command=self.time_starter(self.starters[i]))
            but.grid(column=8, row=i + offset, sticky=tk.W)
            but = tk.Button(self.master, text='Remove',
                            command=self.remove_starter(i))
            but.grid(column=9, row=i + offset, sticky=tk.W)

    def clear_screen(self):  # clear everything from the screen
        list = self.master.grid_slaves()
        for i in list:
            i.destroy()

    def timed_update(self):
        try:
            parts = self.time_start_text.get().split(':')
            h = int(parts[0])
            m = int(parts[1])
            try:
                s = int(parts[2])
            except Exception:
                s = 0
            self.time_start = dt.time(h, m, s)
        except Exception:
            pass
        timeNow = dt.datetime.now().time().replace(microsecond=0)
        self.current_time_text.set(str(timeNow))
        time_elapsed = dt.datetime.combine(dt.date.min, timeNow) \
            - dt.datetime.combine(dt.date.min, self.time_start)
        if timeNow < self.time_start:
            self.elapsed_or_until_start.set('Time Until Start:')
            self.time_elapsed_text.set(str(
                dt.datetime.combine(dt.date.min, self.time_start)
                - dt.datetime.combine(dt.date.min, timeNow)))
        else:
            self.elapsed_or_until_start.set('Time Elapsed:   ')
            self.time_elapsed_text.set(str(time_elapsed))
        self.master.after(100, lambda: self.timed_update())

    def add_starter(self, boat_class):
        '''Returns a function which adds a starter of the given class'''
        def interior_function():
            self.starters.append(Racer())
            self.starters[-1].boat_class = boat_class
            try:
                self.starters[-1].handicap = self.Handicaps[boat_class]
            except Exception:
                self.starters[-1].other = 1
            self.update_display()
        return interior_function

    def remove_starter(self, i):
        '''Returns a function which removes the ith starter'''
        def interior_function():
            message = 'Are you sure you want to remove ' \
                        + self.starters[i].boat_class \
                        + ' ' \
                        + self.starters[i].sail_number.get() \
                        + '?'
            if messagebox.askyesno('Confirm Removal', message):
                del self.starters[i]
                self.update_display()
        return interior_function

    def time_starter(self, boat):
        def interior_function():
            timeNow = dt.datetime.now().time().replace(microsecond=0)
            if timeNow > self.time_start:
                boat.finish_time.set(str(timeNow))
                self.update_display()
        return interior_function

    def rank_starters(self):
        l = []
        for i in range(len(self.starters)):
            try:
                parts = self.starters[i].finish_time.get().split(':')
                h = int(parts[0])
                m = int(parts[1])
                try:
                    s = int(parts[2])
                except Exception:
                    s = 0
                finish_time = dt.time(h, m, s)
                if finish_time < self.time_start:
                    raise
                time_elapsed = dt.datetime.combine(dt.date.min, finish_time) \
                    - dt.datetime.combine(dt.date.min, self.time_start)
                secs = time_elapsed.seconds
                secs_adjusted = round(secs * 1000 / self.starters[i].handicap)
                l.append([i, secs_adjusted])
            except Exception:
                self.starters[i].rank.set('')
        l.sort(key=lambda x: x[1])
        count = 1
        for i in l:
            self.starters[i[0]].rank.set(str(count))
            count += 1

    def sort_starters(self):
        self.rank_starters()
        l = [];
        for i in self.starters:
            try:
                rank_num = int(i.rank.get())
            except Exception:
                rank_num = i.handicap
            l.append([i, rank_num])
        l.sort(key=lambda x: x[1])
        self.starters = []
        for i in l:
            self.starters.append(i[0])
        self.update_display()

    def display_about(self):  # display the about box
        quote1 = self.quotes[random.randrange(len(self.quotes))]
        random.seed()
        quote2 = quote1
        while quote2 == quote1:
            quote2 = self.quotes[random.randrange(len(self.quotes))]
            random.seed()
        aboutText = """
            Sailmbc is a program to simplify the calculation of
            racing results. Created in 2019, Sailmbc has quickly
            become the most popuar sailing software in Oulton
            Broad, and possibly the whole world.\n
            Produced by Adam Yorkston\n
            Tested by Bethany Hood and Kyle Beamish\n
            Unused by Ian Colby\n""" \
            + "-"*len(quote1) + "\n\n"\
            + quote1 + "\n\n" + quote2
        messagebox.showinfo("Sailmbc - everyone's favourite thing!", aboutText)

    def save_as(self):   # asks for the filename and then saves
        try:
            try:
                self.comments = self.comment_box.get("1.0", "end-1c")
            except Exception:
                pass
            curr_directory = os.getcwd()
            filename = filedialog.asksaveasfilename(
                initialdir=curr_directory,
                title="Save As",
                filetypes=(("Sailmbc Files", "*.smb"),),
                defaultextension=".smb")
            picklable_starters = []
            for s in self.starters:
                sdict = {'helm_name': s.helm_name.get(),
                         'sail_number': s.sail_number.get(),
                         'boat_class': s.boat_class,
                         'handicap': s.handicap,
                         'finish_time': s.finish_time.get(),
                         'rank': s.rank.get()}
                picklable_starters.append(sdict)
            saveData = {'picklable_starters': picklable_starters,
                        'time_start_text': self.time_start_text.get(),
                        'race_title_text': self.race_title_text.get(),
                        'comments': self.comments}
            pickle.dump(saveData, open((filename), "wb"))
            self.master.filename = filename
            self.set_title()
        except Exception:
            pass

    def save(self):
        """Tries to save the data using the filename.
        If one doesn't exist, runs saveas
        """
        try:
            try:
                self.comments = self.comment_box.get("1.0", "end-1c")
            except Exception:
                pass
            self.master.filename
            picklable_starters = []
            for s in self.starters:
                sdict = {'helm_name': s.helm_name.get(),
                         'sail_number': s.sail_number.get(),
                         'boat_class': s.boat_class,
                         'handicap': s.handicap,
                         'finish_time': s.finish_time.get(),
                         'rank': s.rank.get()}
                picklable_starters.append(sdict)
            saveData = {'picklable_starters': picklable_starters,
                        'time_start_text': self.time_start_text.get(),
                        'race_title_text': self.race_title_text.get(),
                        'comments': self.comments}
            pickle.dump(saveData, open((self.master.filename), "wb"))
        except Exception:
            self.save_as()

    def load(self):  # Loads the file of one's choosing
        try:
            curr_directory = os.getcwd()
            filename = filedialog.askopenfilename(
                initialdir=curr_directory,
                title="Open File",
                filetypes=(("Sailmbc Files", "*.smb"),))
            if filename == '':
                return
            load_data = pickle.load(open(filename, "rb"))
            self.time_start_text.set(load_data['time_start_text'])
            parts = self.time_start_text.get().split(':')
            h = int(parts[0])
            m = int(parts[1])
            try:
                s = int(parts[2])
            except Exception:
                s = 0
            self.time_start = dt.time(h, m, s)
            self.race_title_text.set(load_data['race_title_text'])
            picklable_starters = load_data['picklable_starters']
            self.starters = []
            for pickled_dict in picklable_starters:
                self.starters.append(Racer())
                self.starters[-1].helm_name.set(pickled_dict['helm_name'])
                self.starters[-1].sail_number.set(pickled_dict['sail_number'])
                self.starters[-1].boat_class = pickled_dict['boat_class']
                self.starters[-1].handicap = pickled_dict['handicap']
                self.starters[-1].finish_time.set(pickled_dict['finish_time'])
                self.starters[-1].rank.set(pickled_dict['rank'])
            self.comments = load_data['comments']
            del self.comment_box
            self.master.filename = filename
            self.set_title()
            self.update_display()
            return 1
        except Exception:
            messagebox.showerror("Error", "The selected file is not readable.")
            return 0

    def print_sailwave(self):
        self.sort_starters()
        html_start = """
        <!DOCTYPE html>
        <html><head>
        <title>Sailmbc results for Waveney &amp;\
            Oulton Broad Yacht Club 2019</title>
        <style type="text/css">
        body {font: 72% arial, helvetica, sans-serif; text-align: center;}
        .hardleft  {text-align: left; float: left;  margin: 15px 0 15px 25px;}
        .hardright {text-align: right; float: right; margin: 15px 25px 15px 0;}
        table {text-align: left; margin: 0px auto 30px auto; font-size: 1em;\
               border-collapse: collapse; border: 1px #fff solid;}
        td, th {padding: 4px; border: 2px #fff solid; vertical-align: top;}
        .caption {padding: 5px; text-align: center; border: 0;\
                  font-weight: bold;}
        h1 {font-size: 1.6em;}
        h2 {font-size: 1.4em;}
        h3 {font-size: 1.2em;}
        p {text-align: center;}
        th {background-color: #aaf;}
        .contents {text-align: left; margin-left: 20%;}
        .even {background-color: #bbf;}
        .odd {background-color: #ddf;}
        .natflag {border: 1px #999 solid;}
        .nattext {font-size: 0.8em;}
        .place1 {font-weight: bold; background-color: #ffffaa;}
        .place2 {font-weight: bold; background-color: #aaaaff;}
        .place3 {font-weight: bold; background-color: #ffaaaa;}
        .placen {}
        </style>
        <script type="text/javascript">
        </script>
        </head>
        <body>
        <header>
        </header>
        <div id="wrap">
        <h1></h1>
        <h2>Waveney &amp; Oulton Broad Yacht Club</h2>
        <div style="clear:both;"></div>
        <style>
        div.applicant-break {page-break-after:always;}
        </style>
        """

        series_title = self.race_title_text.get()

        html_series_title = '<h3 class="series_title">' \
            + series_title + '</h3>\n'
        html_raceDate = '<h3 class="racetitle"\
            id="r1">R1&nbsp;-&nbsp;2019-04-07</h3>\n'
        html_tableHead = """
        <table class="racetable" cellspacing="0" cellpadding="0" border="0">
        <colgroup span="9">
        <col class="rank">
        <col class="class">
        <col class="sailno">
        <col class="boat">
        <col class="helm_name">
        <col class="crewname">
        <col class="rating">
        <col class="elapsed">
        <col class="corrected">
        </colgroup>
        <thead>
        <tr class="titlerow">
        <th>Rank</th>
        <th>Class</th>
        <th>SailNo</th>
        <th>Boat</th>
        <th>helm_name</th>
        <th>CrewName</th>
        <th>PY</th>
        <th>Elapsed</th>
        <th>Corrected</th>
        </tr>
        </thead>
        <tbody>
        """

        html_str = ''
        rclass = '<tr class="odd racerow">'
        count = 6
        for boat in self.starters:
            parts = boat.finish_time.get().split(':')
            if len(parts) == 1 or len(parts) > 3:
                time_elapsed = 'DNF'
                time_adjusted = 'DNF'
            else:
                h = int(parts[0])
                m = int(parts[1])
                try:
                    s = int(parts[2])
                except Exception:
                    s = 0
                finish_time = dt.time(h, m, s)
                if finish_time < self.time_start:
                    raise
                time_elapsed = dt.datetime.combine(dt.date.min, finish_time)\
                    - dt.datetime.combine(dt.date.min, self.time_start)
                secs = time_elapsed.seconds
                secs_adjusted = round(secs * 1000 / boat.handicap)
                time_adjusted = dt.timedelta(seconds=secs_adjusted)
            count += 1
            html_Boat = rclass + """
            <td>{0}</td>
            <td>{1}</td>
            <td>{2}</td>
            <td>&nbsp;</td>
            <td>{3}</td>
            <td>&nbsp;</td>
            <td>{4}</td>
            <td>{5}</td>
            <td>{6}</td>
            </tr>
            """.format(boat.rank.get(),
                       boat.boat_class,
                       boat.sail_number.get(),
                       boat.helm_name.get(),
                       boat.handicap,
                       str(time_elapsed),
                       str(time_adjusted))
            html_str = html_str + html_Boat
            if rclass == '<tr class="odd racerow">':
                rclass = '<tr class="even racerow">'
            else:
                rclass = '<tr class="odd racerow">'

        html_base = """
        </tbody>
        </table>
        </div>
        <footer>
        </footer>
        <div id="scrollbottom"></div>
        </body></html>
        """

        html_str = html_start + html_series_title + html_raceDate \
            + html_tableHead + html_str + html_base

        with open("ResultsSheet.htm", "w") as html_file:
            html_file.write(html_str)

        curr_directory = os.getcwd()
        file_directory = '"' + curr_directory + '\ResultsSheet.htm' + '"'
        os.system("start " + '"title" ' + file_directory)


def new_window():
    win = tk.Toplevel(root)
    win.protocol("WM_DELETE_WINDOW", on_closing(win))
    app = MainApplication(win)
    windows.append(win)
    return app


def load_in_new_window():
    app = new_window()
    if not(app.load()):
        app.master.destroy()
        del windows[windows.index(app.master)]


def on_closing(master):
    def close_checker():
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            master.destroy()
            del windows[windows.index(master)]
        if len(windows) == 0:
            root.destroy()
    return close_checker


windows = []  # keeps track of open windows
root = tk.Tk()
root.withdraw()
new_window()  # opens the first window
root.quit()
root.mainloop()
