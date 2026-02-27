class MESSAGES:
    class RESET:
        ALREADY_INITIALIZED = 'La base de datos ya ha sido inicializada anteriormente.'
    class DATA_FORMAT:
        WRONG_CREDENTIALS_TYPE = 'El formato de las credenciales no es válido. Refiérase a la documentación para más información.'
        ENGINE_URL_ERROR = 'La URL para la conexión a la base de datos no es correcta. El formato debe tener la estructura [postgresql+psycopg2://postgres:<contraseña>@<host_de_la_base_de_datos>:<puerto>/<nombre_de_la_base_de_datos>]'
    class ACCESS:
        NOT_ALLOWED = 'No tienes permiso para realizar esta acción.'
        EXPIRED_TOKEN = 'La sesión del usuario expiró.'
    class ACCOUNT:
        WRONG_PASSWORD = 'Contraseña incorrecta.'
    class TRANSACTION:
        FIELDS_OVERFLOW = 'Solo se puede referenciar un campo a partir del campo relacional. Si se requiere acceder a más tablas, crea un campo computado en ellas para ser usado aquí.'
    class INVALID_STRUCTURE:
        SEARCH_CRITERIA = 'Estructura de criterio de búsqueda inválida.'
