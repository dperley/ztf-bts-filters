# BTS filter in operation from 2020-07-10 to present, converted to Python.

def compiledFunction(current_observation):
    filteron = False
    annotations={}

    # Collect information from the candidate into simple variables
    prevcandidates = current_observation['prv_candidates']
    cand = current_observation['candidate']
    m_now = cand['magpsf']
    m_app = cand['magap']
    t_now = cand['jd']
    fid_now = cand['fid']
    sgscore1 = cand['sgscore1']
    sgscore2 = cand['sgscore2']
    sgscore3 = cand['sgscore3']
    srmag1 = cand['srmag1']
    srmag2 = cand['srmag2']
    srmag3 = cand['srmag3']
    sgmag1 = cand['sgmag1']
    simag1 = cand['simag1']
    szmag1 = cand['szmag1']
    rbscore = cand['rb']
    magnr = cand['magnr']
    distnr = cand['distnr']
    distpsnr1 = cand['distpsnr1']
    distpsnr2 = cand['distpsnr2']
    distpsnr3 = cand['distpsnr3']
    scorr = cand['scorr']
    fwhm = cand['fwhm']
    elong = cand['elong']
    nbad = cand['nbad']
    chipsf = cand['chipsf']
    gal_lat = cand['gal_lat']
    ssdistnr = cand['ssdistnr']
    ssnamenr = cand['ssnamenr']
    ssmagnr = cand['ssmagnr']
    t_start = cand['jdstarthist']
    neargaia = cand['neargaia']
    maggaia = cand['maggaia']
    neargaiabright = cand['neargaiabright']
    maggaiabright = cand['maggaiabright']
    isdiffpos = cand['isdiffpos']
    drb = cand['drb']

    # Define some additional variables
    age = t_now - t_start

    # Set negative distances (no match) to 99 for safety
    if (distpsnr1 < 0):
        distpsnr1 = 99
    if (distpsnr2 < 0):
        distpsnr2 = 99
    if (distpsnr3 < 0):
        distpsnr3 = 99
    if (distnr < 0):
        distnr = 99

    # define a general PS1 magnitude since sometimes bands are missing
    ps1mag = srmag1
    if (ps1mag <= 0 or ps1mag > 30):
        ps1mag = simag1
    if (ps1mag <= 0 or ps1mag > 30):
        ps1mag = sgmag1
    if (ps1mag <= 0 or ps1mag > 30):
        ps1mag = szmag1
    if (ps1mag <= 0):
        ps1mag = 99

    # calculate the PS1 mag in the brightest filter
    ps1maxmag = srmag1
    if (simag1 > 0 and simag1 < ps1maxmag):
        ps1maxmag = simag1
    if (sgmag1 > 0 and sgmag1 < ps1maxmag):
        ps1maxmag = sgmag1
    if (szmag1 > 0 and szmag1 < ps1maxmag):
        ps1maxmag = szmag1
    if (ps1maxmag <= 0):
        ps1maxmag = 99

    # The primary criterion
    bright = m_now < 19.0

    # Require 7 degrees away from Galactic plane
    latitude = True
    if (gal_lat < 7 and gal_lat > (-7)):
        latitude = False

    # Require positive subtraction
    positivesubtraction = False
    if (isdiffpos == 't' or isdiffpos == '1'):
        positivesubtraction = True

    # Require not to be closely coincident with a PS1 star.
    # Is more or less conservative depending on sgscore, brightness, age, and color.
    pointunderneath = False
    if (sgscore1 > 0.76 and distpsnr1 < 2):
        pointunderneath = True
    if (sgscore1 > 0.2 and distpsnr1 < 1):
        if (srmag1 > 0 and szmag1 > 0 and srmag1 - szmag1 > 3.0):
            pointunderneath = True
        if (srmag1 > 0 and simag1 > 0 and srmag1 - simag1 > 3.0):
            pointunderneath = True

    # Require a high RB score.
    # Generally requires RB>0.2 and DRB>0.1, but is more stringent if close to a bright catalogued star
    # and/or has a previous history.
    real = False
    if (rbscore > 0.2):
        real = True
    if (rbscore < 0.35):
        if (neargaia < 1.0 and neargaia > 0.0 and maggaia < 17.0 and maggaia > 0.0):
            real = False
        if (distpsnr1 < 1.0 and (srmag1 > 0 and srmag1 < 17.0 or simag1 > 0 and simag1 < 17.0 or szmag1 > 0 and szmag1 < 16.5) and sgscore1 > 0.49):
            real = False
    if (rbscore < 0.45):
        if (neargaia < 1.5 and neargaia > 0.0 and maggaia < 15.5 and maggaia > 0.0):
            real = False
        if (distpsnr1 < 1.5 and (srmag1 > 0 and srmag1 < 15.5 or simag1 > 0 and simag1 < 15.5 or szmag1 > 0 and szmag1 < 15.0) and sgscore1 > 0.49):
            real = False
    if (drb < 0.1):
        real = False
    if (drb < 0.5):
        if (distpsnr1 < 3.0 and ps1mag < 16 and age > 90):
            real = False
        if (distpsnr1 < 1.1 and ps1mag < 18 and age > 90):
            real = False
    if (drb < 0.8):
        if (distpsnr1 < 1.5 and ps1mag < 15.5 and age > 90):
            real = False
        if (distpsnr1 < 0.8 and ps1mag < 17.5 and age > 90):
            real = False

    # Require not to be in the vicinity of a very bright star.
    brightstar = False
    if (neargaiabright > 0 and neargaiabright < 20 and maggaiabright > 0 and maggaiabright < 12):
        brightstar = True
    if (distpsnr1 < 20 and srmag1 > 0 and srmag1 < 14.0 and sgscore1 > 0.9):
        brightstar = True
    if (distpsnr2 < 20 and srmag2 > 0 and srmag2 < 14.0 and sgscore2 > 0.9):
        brightstar = True
    if (distpsnr3 < 20 and srmag3 > 0 and srmag3 < 14.0 and sgscore3 > 0.9):
        brightstar = True
    if (distpsnr1 < 20 and simag1 > 0 and simag1 < 14.0 and sgscore1 > 0.9):
        brightstar = True
    if (distpsnr1 < 10 and szmag1 > 0 and szmag1 < 14.0 and sgscore1 > 0.9):
        brightstar = True

    # Require at least one previous detection at this position.
    stationary = False
    for prevcandidate in prevcandidates:
        if (prevcandidate['isdiffpos'] == 't' or prevcandidate['isdiffpos'] == '1'):
            dt = t_now - prevcandidate['jd']
            if (dt > 0.02 and prevcandidate['magpsf'] < 99):
                stationary = True

    # Count how many previous detections above 19 mag have occurred and measure the peak magnitude.
    # Also "rescue" any candidates with bright detections in the recent history.
    prevpasscount = 0
    peakmag = 99
    for prevcandidate in prevcandidates:
        if (prevcandidate['isdiffpos'] == 't' or prevcandidate['isdiffpos'] == '1'):
            dt = t_now - prevcandidate['jd']
            if (dt != 0.0 and prevcandidate['magpsf'] < 99):
                if (prevcandidate['fid'] == fid_now):
                    prevbright = prevcandidate['magpsf'] < 19.0
                    if (prevbright):
                        prevpasscount = prevpasscount + 1
                    if (prevcandidate['magpsf'] < peakmag):
                        peakmag = prevcandidate['magpsf']
            if ((dt < 0.75) and (dt > (-0.75)) and (prevcandidate['magpsf'] < 19.0)):
                bright = True

    # See if the source is persistently variable.  Difficult to do with only a 30-day window, but at minimum it must be all of:
    # (a) 90+days old, (b) has passed 19 mag before without being saved, (c) not at <18.5 and rising, 
    # (d) close to a bright reference catalog object.
    variablesource = False
    atmax = (m_now <= peakmag)
    if ((age > 90) and (prevpasscount >= 3 - 1 * (age > 90) - 1 * (age > 360)) and ((not (atmax and m_now < 18.5))) and (magnr > 0)):
        if (distnr < 0.4 and magnr < 19.5):
            variablesource = True
        if (distnr < 0.8 and magnr < 17.5):
            variablesource = True
        if (distnr < 1.2 and magnr < 15.5):
            variablesource = True
    # Alternatively, rule it out as variable if old and very closely coincident with a bright Gaia object.
    if (maggaia > 0 and neargaia > 0):
        if ((neargaia < 0.35) and (maggaia < 17.0) and (age > 30)):
            variablesource = True
        if ((neargaia < 0.35) and (maggaia < 19.0) and (age > 300) and (m_now > 18.5)):
            variablesource = True
        if ((neargaia < 0.2) and (maggaia < 18.0) and (age > 90)):
            variablesource = True
    # Alternatively, rule it out as variable if old and close to a bright PS1 object.  (Formerly pointUnderneath)
    if (sgscore1 > 0.25 and distpsnr1 < 3 and age > 90 and ps1maxmag < 16):
        variablesource = True
    if (sgscore1 == 0.5 and distpsnr1 < 0.5 and age > 90 and ps1maxmag < 17):
        variablesource = True
    # Alternatively, rule it out as variable if old, fainter than its "host", and declining
    if (magnr > 0 and magnr < m_now - 1):
        if ((age > 90) and (distnr < 0.5) and ((not atmax))):
            variablesource = True

    # Check for a close match in the minor planet catalog.  
    rock = False
    rock = (ssdistnr >= 0 and ssdistnr < 12 and ssmagnr < 20)

    # Leave some annotations to be displayed to scanners.
    annotations['jd'] = t_now
    annotations['magnitude'] = m_now
    annotations['age'] = age
    annotations['dt'] = age
    annotations['peakmag'] = peakmag
    annotations['prevpasscount'] = prevpasscount
    annotations['atmax'] = atmax
    annotations['rbscore'] = rbscore
    annotations['magnr'] = magnr
    annotations['distnr'] = distnr
    annotations['srmag1'] = ps1mag
    annotations['distpsnr1'] = distpsnr1
    annotations['sgscore1'] = sgscore1
    annotations['maggaia'] = maggaia
    annotations['neargaia'] = neargaia
    annotations['gal_lat'] = gal_lat
    annotations['drb'] = drb

    # Calculate the filter boolean value (False=fail, True=pass)
    filteron = latitude and bright and ((not pointunderneath)) and stationary and real and positivesubtraction and ((not brightstar)) and ((not rock)) and ((not variablesource))

    return filteron,annotations
