from src.dates.calendar import Calendar
from src.dates.date import Date
import numpy as np

ANBIMA = np.array([
    Date( 1, 1, 2001), Date(26, 2, 2001), Date(27, 2, 2001), Date(13, 4, 2001), Date(21, 4, 2001), Date( 1, 5, 2001),
    Date(14, 6, 2001), Date( 7, 9, 2001), Date(12,10, 2001), Date( 2,11, 2001), Date(15,11, 2001), Date(25,12, 2001), Date( 1, 1, 2002),
    Date(11, 2, 2002), Date(12, 2, 2002), Date(29, 3, 2002), Date(21, 4, 2002), Date( 1, 5, 2002), Date(30, 5, 2002), Date( 7, 9, 2002),
    Date(12,10, 2002), Date( 2,11, 2002), Date(15,11, 2002), Date(25,12, 2002), Date( 1, 1, 2003), Date( 3, 3, 2003), Date( 4, 3, 2003),
    Date(18, 4, 2003), Date(21, 4, 2003), Date( 1, 5, 2003), Date(19, 6, 2003), Date( 7, 9, 2003), Date(12,10, 2003), Date( 2,11, 2003),
    Date(15,11, 2003), Date(25,12, 2003), Date( 1, 1, 2004), Date(23, 2, 2004), Date(24, 2, 2004), Date( 9, 4, 2004), Date(21, 4, 2004),
    Date( 1, 5, 2004), Date(10, 6, 2004), Date( 7, 9, 2004), Date(12,10, 2004), Date( 2,11, 2004), Date(15,11, 2004), Date(25,12, 2004),
    Date( 1, 1, 2005), Date( 7, 2, 2005), Date( 8, 2, 2005), Date(25, 3, 2005), Date(21, 4, 2005), Date( 1, 5, 2005), Date(26, 5, 2005),
    Date( 7, 9, 2005), Date(12,10, 2005), Date( 2,11, 2005), Date(15,11, 2005), Date(25,12, 2005), Date( 1, 1, 2006), Date(27, 2, 2006),
    Date(28, 2, 2006), Date(14, 4, 2006), Date(21, 4, 2006), Date( 1, 5, 2006), Date(15, 6, 2006), Date( 7, 9, 2006), Date(12,10, 2006),
    Date( 2,11, 2006), Date(15,11, 2006), Date(25,12, 2006), Date( 1, 1, 2007), Date(19, 2, 2007), Date(20, 2, 2007), Date( 6, 4, 2007),
    Date(21, 4, 2007), Date( 1, 5, 2007), Date( 7, 6, 2007), Date( 7, 9, 2007), Date(12,10, 2007), Date( 2,11, 2007), Date(15,11, 2007),
    Date(25,12, 2007), Date( 1, 1, 2008), Date( 4, 2, 2008), Date( 5, 2, 2008), Date(21, 3, 2008), Date(21, 4, 2008), Date( 1, 5, 2008),
    Date(22, 5, 2008), Date( 7, 9, 2008), Date(12,10, 2008), Date( 2,11, 2008), Date(15,11, 2008), Date(25,12, 2008), Date( 1, 1, 2009),
    Date(23, 2, 2009), Date(24, 2, 2009), Date(10, 4, 2009), Date(21, 4, 2009), Date( 1, 5, 2009), Date(11, 6, 2009), Date( 7, 9, 2009),
    Date(12,10, 2009), Date( 2,11, 2009), Date(15,11, 2009), Date(25,12, 2009), Date( 1, 1, 2010), Date(15, 2, 2010), Date(16, 2, 2010),
    Date( 2, 4, 2010), Date(21, 4, 2010), Date( 1, 5, 2010), Date( 3, 6, 2010), Date( 7, 9, 2010), Date(12,10, 2010), Date( 2,11, 2010),
    Date(15,11, 2010), Date(25,12, 2010), Date( 1, 1, 2011), Date( 7, 3, 2011), Date( 8, 3, 2011), Date(21, 4, 2011), Date(22, 4, 2011),
    Date( 1, 5, 2011), Date(23, 6, 2011), Date( 7, 9, 2011), Date(12,10, 2011), Date( 2,11, 2011), Date(15,11, 2011), Date(25,12, 2011),
    Date( 1, 1, 2012), Date(20, 2, 2012), Date(21, 2, 2012), Date( 6, 4, 2012), Date(21, 4, 2012), Date( 1, 5, 2012), Date( 7, 6, 2012),
    Date( 7, 9, 2012), Date(12,10, 2012), Date( 2,11, 2012), Date(15,11, 2012), Date(25,12, 2012), Date( 1, 1, 2013), Date(11, 2, 2013),
    Date(12, 2, 2013), Date(29, 3, 2013), Date(21, 4, 2013), Date( 1, 5, 2013), Date(30, 5, 2013), Date( 7, 9, 2013), Date(12,10, 2013),
    Date( 2,11, 2013), Date(15,11, 2013), Date(25,12, 2013), Date( 1, 1, 2014), Date( 3, 3, 2014), Date( 4, 3, 2014), Date(18, 4, 2014),
    Date(21, 4, 2014), Date( 1, 5, 2014), Date(19, 6, 2014), Date( 7, 9, 2014), Date(12,10, 2014), Date( 2,11, 2014), Date(15,11, 2014),
    Date(25,12, 2014), Date( 1, 1, 2015), Date(16, 2, 2015), Date(17, 2, 2015), Date( 3, 4, 2015), Date(21, 4, 2015), Date( 1, 5, 2015),
    Date( 4, 6, 2015), Date( 7, 9, 2015), Date(12,10, 2015), Date( 2,11, 2015), Date(15,11, 2015), Date(25,12, 2015), Date( 1, 1, 2016),
    Date( 8, 2, 2016), Date( 9, 2, 2016), Date(25, 3, 2016), Date(21, 4, 2016), Date( 1, 5, 2016), Date(26, 5, 2016), Date( 7, 9, 2016),
    Date(12,10, 2016), Date( 2,11, 2016), Date(15,11, 2016), Date(25,12, 2016), Date( 1, 1, 2017), Date(27, 2, 2017), Date(28, 2, 2017),
    Date(14, 4, 2017), Date(21, 4, 2017), Date( 1, 5, 2017), Date(15, 6, 2017), Date( 7, 9, 2017), Date(12,10, 2017), Date( 2,11, 2017),
    Date(15,11, 2017), Date(25,12, 2017), Date( 1, 1, 2018), Date(12, 2, 2018), Date(13, 2, 2018), Date(30, 3, 2018), Date(21, 4, 2018),
    Date( 1, 5, 2018), Date(31, 5, 2018), Date( 7, 9, 2018), Date(12,10, 2018), Date( 2,11, 2018), Date(15,11, 2018), Date(25,12, 2018),
    Date( 1, 1, 2019), Date( 4, 3, 2019), Date( 5, 3, 2019), Date(19, 4, 2019), Date(21, 4, 2019), Date( 1, 5, 2019), Date(20, 6, 2019),
    Date( 7, 9, 2019), Date(12,10, 2019), Date( 2,11, 2019), Date(15,11, 2019), Date(25,12, 2019), Date( 1, 1, 2020), Date(24, 2, 2020),
    Date(25, 2, 2020), Date(10, 4, 2020), Date(21, 4, 2020), Date( 1, 5, 2020), Date(11, 6, 2020), Date( 7, 9, 2020), Date(12,10, 2020),
    Date( 2,11, 2020), Date(15,11, 2020), Date(25,12, 2020), Date( 1, 1, 2021), Date(15, 2, 2021), Date(16, 2, 2021), Date( 2, 4, 2021),
    Date(21, 4, 2021), Date( 1, 5, 2021), Date( 3, 6, 2021), Date( 7, 9, 2021), Date(12,10, 2021), Date( 2,11, 2021), Date(15,11, 2021),
    Date(25,12, 2021), Date( 1, 1, 2022), Date(28, 2, 2022), Date( 1, 3, 2022), Date(15, 4, 2022), Date(21, 4, 2022), Date( 1, 5, 2022),
    Date(16, 6, 2022), Date( 7, 9, 2022), Date(12,10, 2022), Date( 2,11, 2022), Date(15,11, 2022), Date(25,12, 2022), Date( 1, 1, 2023),
    Date(20, 2, 2023), Date(21, 2, 2023), Date( 7, 4, 2023), Date(21, 4, 2023), Date( 1, 5, 2023), Date( 8, 6, 2023), Date( 7, 9, 2023),
    Date(12,10, 2023), Date( 2,11, 2023), Date(15,11, 2023), Date(25,12, 2023), Date( 1, 1, 2024), Date(12, 2, 2024), Date(13, 2, 2024),
    Date(29, 3, 2024), Date(21, 4, 2024), Date( 1, 5, 2024), Date(30, 5, 2024), Date( 7, 9, 2024), Date(12,10, 2024), Date( 2,11, 2024),
    Date(15,11, 2024), Date(25,12, 2024), Date( 1, 1, 2025), Date( 3, 3, 2025), Date( 4, 3, 2025), Date(18, 4, 2025), Date(21, 4, 2025),
    Date( 1, 5, 2025), Date(19, 6, 2025), Date( 7, 9, 2025), Date(12,10, 2025), Date( 2,11, 2025), Date(15,11, 2025), Date(25,12, 2025),
    Date( 1, 1, 2026), Date(16, 2, 2026), Date(17, 2, 2026), Date( 3, 4, 2026), Date(21, 4, 2026), Date( 1, 5, 2026), Date( 4, 6, 2026),
    Date( 7, 9, 2026), Date(12,10, 2026), Date( 2,11, 2026), Date(15,11, 2026), Date(25,12, 2026), Date( 1, 1, 2027), Date( 8, 2, 2027),
    Date( 9, 2, 2027), Date(26, 3, 2027), Date(21, 4, 2027), Date( 1, 5, 2027), Date(27, 5, 2027), Date( 7, 9, 2027), Date(12,10, 2027),
    Date( 2,11, 2027), Date(15,11, 2027), Date(25,12, 2027), Date( 1, 1, 2028), Date(28, 2, 2028), Date(29, 2, 2028), Date(14, 4, 2028),
    Date(21, 4, 2028), Date( 1, 5, 2028), Date(15, 6, 2028), Date( 7, 9, 2028), Date(12,10, 2028), Date( 2,11, 2028), Date(15,11, 2028),
    Date(25,12, 2028), Date( 1, 1, 2029), Date(12, 2, 2029), Date(13, 2, 2029), Date(30, 3, 2029), Date(21, 4, 2029), Date( 1, 5, 2029),
    Date(31, 5, 2029), Date( 7, 9, 2029), Date(12,10, 2029), Date( 2,11, 2029), Date(15,11, 2029), Date(25,12, 2029), Date( 1, 1, 2030),
    Date( 4, 3, 2030), Date( 5, 3, 2030), Date(19, 4, 2030), Date(21, 4, 2030), Date( 1, 5, 2030), Date(20, 6, 2030), Date( 7, 9, 2030),
    Date(12,10, 2030), Date( 2,11, 2030), Date(15,11, 2030), Date(25,12, 2030), Date( 1, 1, 2031), Date(24, 2, 2031), Date(25, 2, 2031),
    Date(11, 4, 2031), Date(21, 4, 2031), Date( 1, 5, 2031), Date(12, 6, 2031), Date( 7, 9, 2031), Date(12,10, 2031), Date( 2,11, 2031),
    Date(15,11, 2031), Date(25,12, 2031), Date( 1, 1, 2032), Date( 9, 2, 2032), Date(10, 2, 2032), Date(26, 3, 2032), Date(21, 4, 2032),
    Date( 1, 5, 2032), Date(27, 5, 2032), Date( 7, 9, 2032), Date(12,10, 2032), Date( 2,11, 2032), Date(15,11, 2032), Date(25,12, 2032),
    Date( 1, 1, 2033), Date(28, 2, 2033), Date( 1, 3, 2033), Date(15, 4, 2033), Date(21, 4, 2033), Date( 1, 5, 2033), Date(16, 6, 2033),
    Date( 7, 9, 2033), Date(12,10, 2033), Date( 2,11, 2033), Date(15,11, 2033), Date(25,12, 2033), Date( 1, 1, 2034), Date(20, 2, 2034),
    Date(21, 2, 2034), Date( 7, 4, 2034), Date(21, 4, 2034), Date( 1, 5, 2034), Date( 8, 6, 2034), Date( 7, 9, 2034), Date(12,10, 2034),
    Date( 2,11, 2034), Date(15,11, 2034), Date(25,12, 2034), Date( 1, 1, 2035), Date( 5, 2, 2035), Date( 6, 2, 2035), Date(23, 3, 2035),
    Date(21, 4, 2035), Date( 1, 5, 2035), Date(24, 5, 2035), Date( 7, 9, 2035), Date(12,10, 2035), Date( 2,11, 2035), Date(15,11, 2035),
    Date(25,12, 2035), Date( 1, 1, 2036), Date(25, 2, 2036), Date(26, 2, 2036), Date(11, 4, 2036), Date(21, 4, 2036), Date( 1, 5, 2036),
    Date(12, 6, 2036), Date( 7, 9, 2036), Date(12,10, 2036), Date( 2,11, 2036), Date(15,11, 2036), Date(25,12, 2036), Date( 1, 1, 2037),
    Date(16, 2, 2037), Date(17, 2, 2037), Date( 3, 4, 2037), Date(21, 4, 2037), Date( 1, 5, 2037), Date( 4, 6, 2037), Date( 7, 9, 2037),
    Date(12,10, 2037), Date( 2,11, 2037), Date(15,11, 2037), Date(25,12, 2037), Date( 1, 1, 2038), Date( 8, 3, 2038), Date( 9, 3, 2038),
    Date(21, 4, 2038), Date(23, 4, 2038), Date( 1, 5, 2038), Date(24, 6, 2038), Date( 7, 9, 2038), Date(12,10, 2038), Date( 2,11, 2038),
    Date(15,11, 2038), Date(25,12, 2038), Date( 1, 1, 2039), Date(21, 2, 2039), Date(22, 2, 2039), Date( 8, 4, 2039), Date(21, 4, 2039),
    Date( 1, 5, 2039), Date( 9, 6, 2039), Date( 7, 9, 2039), Date(12,10, 2039), Date( 2,11, 2039), Date(15,11, 2039), Date(25,12, 2039),
    Date( 1, 1, 2040), Date(13, 2, 2040), Date(14, 2, 2040), Date(30, 3, 2040), Date(21, 4, 2040), Date( 1, 5, 2040), Date(31, 5, 2040),
    Date( 7, 9, 2040), Date(12,10, 2040), Date( 2,11, 2040), Date(15,11, 2040), Date(25,12, 2040), Date( 1, 1, 2041), Date( 4, 3, 2041),
    Date( 5, 3, 2041), Date(19, 4, 2041), Date(21, 4, 2041), Date( 1, 5, 2041), Date(20, 6, 2041), Date( 7, 9, 2041), Date(12,10, 2041),
    Date( 2,11, 2041), Date(15,11, 2041), Date(25,12, 2041), Date( 1, 1, 2042), Date(17, 2, 2042), Date(18, 2, 2042), Date( 4, 4, 2042),
    Date(21, 4, 2042), Date( 1, 5, 2042), Date( 5, 6, 2042), Date( 7, 9, 2042), Date(12,10, 2042), Date( 2,11, 2042), Date(15,11, 2042),
    Date(25,12, 2042), Date( 1, 1, 2043), Date( 9, 2, 2043), Date(10, 2, 2043), Date(27, 3, 2043), Date(21, 4, 2043), Date( 1, 5, 2043),
    Date(28, 5, 2043), Date( 7, 9, 2043), Date(12,10, 2043), Date( 2,11, 2043), Date(15,11, 2043), Date(25,12, 2043), Date( 1, 1, 2044),
    Date(29, 2, 2044), Date( 1, 3, 2044), Date(15, 4, 2044), Date(21, 4, 2044), Date( 1, 5, 2044), Date(16, 6, 2044), Date( 7, 9, 2044),
    Date(12,10, 2044), Date( 2,11, 2044), Date(15,11, 2044), Date(25,12, 2044), Date( 1, 1, 2045), Date(20, 2, 2045), Date(21, 2, 2045),
    Date( 7, 4, 2045), Date(21, 4, 2045), Date( 1, 5, 2045), Date( 8, 6, 2045), Date( 7, 9, 2045), Date(12,10, 2045), Date( 2,11, 2045),
    Date(15,11, 2045), Date(25,12, 2045), Date( 1, 1, 2046), Date( 5, 2, 2046), Date( 6, 2, 2046), Date(23, 3, 2046), Date(21, 4, 2046),
    Date( 1, 5, 2046), Date(24, 5, 2046), Date( 7, 9, 2046), Date(12,10, 2046), Date( 2,11, 2046), Date(15,11, 2046), Date(25,12, 2046),
    Date( 1, 1, 2047), Date(25, 2, 2047), Date(26, 2, 2047), Date(12, 4, 2047), Date(21, 4, 2047), Date( 1, 5, 2047), Date(13, 6, 2047),
    Date( 7, 9, 2047), Date(12,10, 2047), Date( 2,11, 2047), Date(15,11, 2047), Date(25,12, 2047), Date( 1, 1, 2048), Date(17, 2, 2048),
    Date(18, 2, 2048), Date( 3, 4, 2048), Date(21, 4, 2048), Date( 1, 5, 2048), Date( 4, 6, 2048), Date( 7, 9, 2048), Date(12,10, 2048),
    Date( 2,11, 2048), Date(15,11, 2048), Date(25,12, 2048), Date( 1, 1, 2049), Date( 1, 3, 2049), Date( 2, 3, 2049), Date(16, 4, 2049),
    Date(21, 4, 2049), Date( 1, 5, 2049), Date(17, 6, 2049), Date( 7, 9, 2049), Date(12,10, 2049), Date( 2,11, 2049), Date(15,11, 2049),
    Date(25,12, 2049), Date( 1, 1, 2050), Date(21, 2, 2050), Date(22, 2, 2050), Date( 8, 4, 2050), Date(21, 4, 2050), Date( 1, 5, 2050),
    Date( 9, 6, 2050), Date( 7, 9, 2050), Date(12,10, 2050), Date( 2,11, 2050), Date(15,11, 2050), Date(25,12, 2050), Date( 1, 1, 2051),
    Date(13, 2, 2051), Date(14, 2, 2051), Date(31, 3, 2051), Date(21, 4, 2051), Date( 1, 5, 2051), Date( 1, 6, 2051), Date( 7, 9, 2051),
    Date(12,10, 2051), Date( 2,11, 2051), Date(15,11, 2051), Date(25,12, 2051), Date( 1, 1, 2052), Date( 4, 3, 2052), Date( 5, 3, 2052),
    Date(19, 4, 2052), Date(21, 4, 2052), Date( 1, 5, 2052), Date(20, 6, 2052), Date( 7, 9, 2052), Date(12,10, 2052), Date( 2,11, 2052),
    Date(15,11, 2052), Date(25,12, 2052), Date( 1, 1, 2053), Date(17, 2, 2053), Date(18, 2, 2053), Date( 4, 4, 2053), Date(21, 4, 2053),
    Date( 1, 5, 2053), Date( 5, 6, 2053), Date( 7, 9, 2053), Date(12,10, 2053), Date( 2,11, 2053), Date(15,11, 2053), Date(25,12, 2053),
    Date( 1, 1, 2054), Date( 9, 2, 2054), Date(10, 2, 2054), Date(27, 3, 2054), Date(21, 4, 2054), Date( 1, 5, 2054), Date(28, 5, 2054),
    Date( 7, 9, 2054), Date(12,10, 2054), Date( 2,11, 2054), Date(15,11, 2054), Date(25,12, 2054), Date( 1, 1, 2055), Date( 1, 3, 2055),
    Date( 2, 3, 2055), Date(16, 4, 2055), Date(21, 4, 2055), Date( 1, 5, 2055), Date(17, 6, 2055), Date( 7, 9, 2055), Date(12,10, 2055),
    Date( 2,11, 2055), Date(15,11, 2055), Date(25,12, 2055), Date( 1, 1, 2056), Date(14, 2, 2056), Date(15, 2, 2056), Date(31, 3, 2056),
    Date(21, 4, 2056), Date( 1, 5, 2056), Date( 1, 6, 2056), Date( 7, 9, 2056), Date(12,10, 2056), Date( 2,11, 2056), Date(15,11, 2056),
    Date(25,12, 2056), Date( 1, 1, 2057), Date( 5, 3, 2057), Date( 6, 3, 2057), Date(20, 4, 2057), Date(21, 4, 2057), Date( 1, 5, 2057),
    Date(21, 6, 2057), Date( 7, 9, 2057), Date(12,10, 2057), Date( 2,11, 2057), Date(15,11, 2057), Date(25,12, 2057), Date( 1, 1, 2058),
    Date(25, 2, 2058), Date(26, 2, 2058), Date(12, 4, 2058), Date(21, 4, 2058), Date( 1, 5, 2058), Date(13, 6, 2058), Date( 7, 9, 2058),
    Date(12,10, 2058), Date( 2,11, 2058), Date(15,11, 2058), Date(25,12, 2058), Date( 1, 1, 2059), Date(10, 2, 2059), Date(11, 2, 2059),
    Date(28, 3, 2059), Date(21, 4, 2059), Date( 1, 5, 2059), Date(29, 5, 2059), Date( 7, 9, 2059), Date(12,10, 2059), Date( 2,11, 2059),
    Date(15,11, 2059), Date(25,12, 2059), Date( 1, 1, 2060), Date( 1, 3, 2060), Date( 2, 3, 2060), Date(16, 4, 2060), Date(21, 4, 2060),
    Date( 1, 5, 2060), Date(17, 6, 2060), Date( 7, 9, 2060), Date(12,10, 2060), Date( 2,11, 2060), Date(15,11, 2060), Date(25,12, 2060),
    Date( 1, 1, 2061), Date(21, 2, 2061), Date(22, 2, 2061), Date( 8, 4, 2061), Date(21, 4, 2061), Date( 1, 5, 2061), Date( 9, 6, 2061),
    Date( 7, 9, 2061), Date(12,10, 2061), Date( 2,11, 2061), Date(15,11, 2061), Date(25,12, 2061), Date( 1, 1, 2062), Date( 6, 2, 2062),
    Date( 7, 2, 2062), Date(24, 3, 2062), Date(21, 4, 2062), Date( 1, 5, 2062), Date(25, 5, 2062), Date( 7, 9, 2062), Date(12,10, 2062),
    Date( 2,11, 2062), Date(15,11, 2062), Date(25,12, 2062), Date( 1, 1, 2063), Date(26, 2, 2063), Date(27, 2, 2063), Date(13, 4, 2063),
    Date(21, 4, 2063), Date( 1, 5, 2063), Date(14, 6, 2063), Date( 7, 9, 2063), Date(12,10, 2063), Date( 2,11, 2063), Date(15,11, 2063),
    Date(25,12, 2063), Date( 1, 1, 2064), Date(18, 2, 2064), Date(19, 2, 2064), Date( 4, 4, 2064), Date(21, 4, 2064), Date( 1, 5, 2064),
    Date( 5, 6, 2064), Date( 7, 9, 2064), Date(12,10, 2064), Date( 2,11, 2064), Date(15,11, 2064), Date(25,12, 2064), Date( 1, 1, 2065),
    Date( 9, 2, 2065), Date(10, 2, 2065), Date(27, 3, 2065), Date(21, 4, 2065), Date( 1, 5, 2065), Date(28, 5, 2065), Date( 7, 9, 2065),
    Date(12,10, 2065), Date( 2,11, 2065), Date(15,11, 2065), Date(25,12, 2065), Date( 1, 1, 2066), Date(22, 2, 2066), Date(23, 2, 2066),
    Date( 9, 4, 2066), Date(21, 4, 2066), Date( 1, 5, 2066), Date(10, 6, 2066), Date( 7, 9, 2066), Date(12,10, 2066), Date( 2,11, 2066),
    Date(15,11, 2066), Date(25,12, 2066), Date( 1, 1, 2067), Date(14, 2, 2067), Date(15, 2, 2067), Date( 1, 4, 2067), Date(21, 4, 2067),
    Date( 1, 5, 2067), Date( 2, 6, 2067), Date( 7, 9, 2067), Date(12,10, 2067), Date( 2,11, 2067), Date(15,11, 2067), Date(25,12, 2067),
    Date( 1, 1, 2068), Date( 5, 3, 2068), Date( 6, 3, 2068), Date(20, 4, 2068), Date(21, 4, 2068), Date( 1, 5, 2068), Date(21, 6, 2068),
    Date( 7, 9, 2068), Date(12,10, 2068), Date( 2,11, 2068), Date(15,11, 2068), Date(25,12, 2068), Date( 1, 1, 2069), Date(25, 2, 2069),
    Date(26, 2, 2069), Date(12, 4, 2069), Date(21, 4, 2069), Date( 1, 5, 2069), Date(13, 6, 2069), Date( 7, 9, 2069), Date(12,10, 2069),
    Date( 2,11, 2069), Date(15,11, 2069), Date(25,12, 2069), Date( 1, 1, 2070), Date(10, 2, 2070), Date(11, 2, 2070), Date(28, 3, 2070),
    Date(21, 4, 2070), Date( 1, 5, 2070), Date(29, 5, 2070), Date( 7, 9, 2070), Date(12,10, 2070), Date( 2,11, 2070), Date(15,11, 2070),
    Date(25,12, 2070), Date( 1, 1, 2071), Date( 2, 3, 2071), Date( 3, 3, 2071), Date(17, 4, 2071), Date(21, 4, 2071), Date( 1, 5, 2071),
    Date(18, 6, 2071), Date( 7, 9, 2071), Date(12,10, 2071), Date( 2,11, 2071), Date(15,11, 2071), Date(25,12, 2071), Date( 1, 1, 2072),
    Date(22, 2, 2072), Date(23, 2, 2072), Date( 8, 4, 2072), Date(21, 4, 2072), Date( 1, 5, 2072), Date( 9, 6, 2072), Date( 7, 9, 2072),
    Date(12,10, 2072), Date( 2,11, 2072), Date(15,11, 2072), Date(25,12, 2072), Date( 1, 1, 2073), Date( 6, 2, 2073), Date( 7, 2, 2073),
    Date(24, 3, 2073), Date(21, 4, 2073), Date( 1, 5, 2073), Date(25, 5, 2073), Date( 7, 9, 2073), Date(12,10, 2073), Date( 2,11, 2073),
    Date(15,11, 2073), Date(25,12, 2073), Date( 1, 1, 2074), Date(26, 2, 2074), Date(27, 2, 2074), Date(13, 4, 2074), Date(21, 4, 2074),
    Date( 1, 5, 2074), Date(14, 6, 2074), Date( 7, 9, 2074), Date(12,10, 2074), Date( 2,11, 2074), Date(15,11, 2074), Date(25,12, 2074),
    Date( 1, 1, 2075), Date(18, 2, 2075), Date(19, 2, 2075), Date( 5, 4, 2075), Date(21, 4, 2075), Date( 1, 5, 2075), Date( 6, 6, 2075),
    Date( 7, 9, 2075), Date(12,10, 2075), Date( 2,11, 2075), Date(15,11, 2075), Date(25,12, 2075), Date( 1, 1, 2076), Date( 2, 3, 2076),
    Date( 3, 3, 2076), Date(17, 4, 2076), Date(21, 4, 2076), Date( 1, 5, 2076), Date(18, 6, 2076), Date( 7, 9, 2076), Date(12,10, 2076),
    Date( 2,11, 2076), Date(15,11, 2076), Date(25,12, 2076), Date( 1, 1, 2077), Date(22, 2, 2077), Date(23, 2, 2077), Date( 9, 4, 2077),
    Date(21, 4, 2077), Date( 1, 5, 2077), Date(10, 6, 2077), Date( 7, 9, 2077), Date(12,10, 2077), Date( 2,11, 2077), Date(15,11, 2077),
    Date(25,12, 2077), Date( 1, 1, 2078), Date(14, 2, 2078), Date(15, 2, 2078), Date( 1, 4, 2078), Date(21, 4, 2078), Date( 1, 5, 2078),
    Date( 2, 6, 2078), Date( 7, 9, 2078), Date(12,10, 2078), Date( 2,11, 2078), Date(15,11, 2078), Date(25,12, 2078), Date( 1, 1, 2079)
])

class Brazil(Calendar):
    def __init__(self):
        super(Brazil, self).__init__()

    def isHoliday(self, date):
        if super(Brazil, self).isHoliday(date): return True
        for i in ANBIMA:
            if (date == i): return True
        return False

    def businessDaysBetween(self, date_from: Date, date_to: Date):
        d = super().businessDaysBetween(date_from, date_to)

        return d


if __name__ == "__main__":
    cal = Brazil()
    gen = Calendar()
    print( Date(1, 1, 2019) - Date(1, 1, 2018) )
    print( gen.businessDaysBetween(Date( 1, 1, 2018), Date( 1, 1, 2019)) )
    print( cal.businessDaysBetween(Date(1, 1, 2018), Date(1, 1, 2019)) )
    print(np.where(Date(1, 1, 2018) < ANBIMA and Date(1, 1, 2019) > ANBIMA))