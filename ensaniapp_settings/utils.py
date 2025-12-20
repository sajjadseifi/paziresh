import jdatetime
def _parse_jdate(self, value: str):
    """
    تبدیل '1404-10-01' یا '1404/10/01' به jdatetime.date
    """
    if not value:
        return None

    value = value.replace('-', '/')
    y, m, d = map(int, value.split('/'))
    return jdatetime.date(y, m, d)
