DISTNAME=	buildbot
CATEGORIES=	meta-pkgs
MASTER_SITES=	"https://buildbot.net"

MAINTAINER=	uki@NetBSD.org
COMMENT=	Meta package for buildbot master and worker

DEPENDS+=	${PYPKGPREFIX}-sqlite3-[0-9]*:../../database/py-sqlite3
DEPENDS+=	${PYPKGPREFIX}-buildbot-[0-9]*:../../devel/py-buildbot
DEPENDS+=	${PYPKGPREFIX}-buildbot-console-view-[0-9]*:../../devel/py-buildbot-console-view
DEPENDS+=	${PYPKGPREFIX}-buildbot-grid-view-[0-9]*:../../devel/py-buildbot-grid-view
DEPENDS+=	${PYPKGPREFIX}-buildbot-pkg-[0-9]*:../../devel/py-buildbot-pkg
DEPENDS+=	${PYPKGPREFIX}-buildbot-waterfall-view-[0-9]*:../../devel/py-buildbot-waterfall-view
DEPENDS+=	${PYPKGPREFIX}-buildbot-worker-[0-9]*:../../devel/py-buildbot-worker
DEPENDS+=	${PYPKGPREFIX}-buildbot-www-[0-9]*:../../devel/py-buildbot-www

META_PACKAGE=	yes

.include "../../lang/python/egg.mk"
.include "../../mk/bsd.pkg.mk"
