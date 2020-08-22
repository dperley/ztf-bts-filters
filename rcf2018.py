# BTS filter in operation from 2018-05 to 2019-03-27, converted to Python.
# A slightly modified version was used after 2019-03-27 and until 2019-06-12:
#  (sgscore == 0.5 and distpsnr1 < 0.5 and (sgmag < 17 or srmag < 17 or simag < 17))
#  was added as an extra condition for brightstar = True.

def compiledFunction(current_observation):
    filteron = False
    annotations={}
    bright = False
    nopointunderneath = True
    mover = True
    real = False
    slope = 0.0
    t_slope = 0.0
    rb = 0.0
    positivesubtraction = False
    brightstar = False
    scorr = 0.0
    latitude = True
    prevcandidates = current_observation['prv_candidates']
    m_now = current_observation['candidate']['magpsf']
    m_app = current_observation['candidate']['magap']
    t_now = current_observation['candidate']['jd']
    fid_now = current_observation['candidate']['fid']
    sgscore = current_observation['candidate']['sgscore1']
    sgscore2 = current_observation['candidate']['sgscore2']
    sgscore3 = current_observation['candidate']['sgscore3']
    srmag = current_observation['candidate']['srmag1']
    srmag2 = current_observation['candidate']['srmag2']
    srmag3 = current_observation['candidate']['srmag3']
    sgmag = current_observation['candidate']['sgmag1']
    simag = current_observation['candidate']['simag1']
    rbscore = current_observation['candidate']['rb']
    magnr = current_observation['candidate']['magnr']
    distnr = current_observation['candidate']['distnr']
    distpsnr1 = current_observation['candidate']['distpsnr1']
    distpsnr2 = current_observation['candidate']['distpsnr2']
    distpsnr3 = current_observation['candidate']['distpsnr3']
    scorr = current_observation['candidate']['scorr']
    fwhm = current_observation['candidate']['fwhm']
    elong = current_observation['candidate']['elong']
    nbad = current_observation['candidate']['nbad']
    chipsf = current_observation['candidate']['chipsf']
    gal_lat = current_observation['candidate']['gal_lat']

    # The primary criterion
    bright = m_now < 19.0

    # Require 7 degrees away from Galactic plane
    if (gal_lat and gal_lat < 7 and gal_lat > (-7)):
        latitude = False

    # Require positive subtraction
    if (current_observation['candidate']['isdiffpos'] and (current_observation['candidate']['isdiffpos'] == 't' or current_observation['candidate']['isdiffpos'] == '1')):
        positivesubtraction = True

    # Require a high RB score.
    if (rbscore and rbscore > 0.2):
        real = True

    # Require not to be closely coincident with a PS1 star
    if (sgscore and distpsnr1 and sgscore > 0.76 and distpsnr1 < 2):
        nopointunderneath = False

    # Require not to be in the vicinity of a very bright star
    if ((distpsnr1 and srmag and distpsnr1 < 20 and srmag < 16.0 and srmag>0 and sgscore > 0.49) or \
        (distpsnr2 and srmag2 and distpsnr2 < 20 and srmag2 < 16.0 and srmag2>0 and sgscore2 > 0.49) or \
        (distpsnr3 and srmag3 and distpsnr3 < 20 and srmag3 < 16.0 and srmag3>0 and sgscore3 > 0.49) ):
        brightstar = True

    # Require at least one previous detection at this position
    for candidate in prevcandidates:
        if (candidate['jd'] and candidate['magpsf'] and candidate['fid'] and candidate['isdiffpos'] and (candidate['isdiffpos'] == 't' or candidate['isdiffpos'] == '1')):
            dt = t_now - candidate['jd']
            if (dt > 0.02 and candidate['magpsf'] < 99):
                mover = False
            if (dt != 0.0 and candidate['magpsf'] < 99):
                if (candidate['jd'] > t_slope and candidate['fid'] == fid_now):
                    t_slope = candidate['jd']
                    slope = (m_now - candidate['magpsf']) / dt

    annotations['magnitude'] = m_now
    annotations['sgscore'] = sgscore
    annotations['slope'] = slope
    annotations['rbscore'] = rbscore
    annotations['mover'] = mover
    annotations['real'] = real
    annotations['positiveSubtraction'] = positivesubtraction
    annotations['brightStar'] = brightstar
    annotations['magnr'] = magnr
    annotations['distnr'] = distnr
    annotations['scorr'] = scorr
    annotations['gal_lat'] = gal_lat

    filteron = bright and nopointunderneath and ((not mover)) and real and positivesubtraction and ((not brightstar))
    return filteron,annotations
