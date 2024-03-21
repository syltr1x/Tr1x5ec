### Config Explanation
"singleaesforfile"    -> Esto indica si se usara una clave AES unica para cada archivo (usuario, email, contraseña) 1=True, 0=False (Aconsejamos dejarlo en 1)
"aesforrsa"           -> Determina si las claves rsa (algo.pri.pem) seran cifradas usand AES (igual que el anterior 1=True, 0=False)
"singleaesforrsa"     -> Permite decidir si queremos una clave AES unica para cada las claves RSA (pub y priv) (1=True, 0=False)
"singlersaforkey"     -> En caso de querer crear una clave RSA propia para cifrar la llave de cuenta (1=True, 0=False)
"restorekey"          -> Brinda el poder reestablecer la key usando TODAS las credenciales de la cuenta (0=False, 1=True) (ACONSEJAMOS DEJAR ESTA OPCION EN 0)
"fieldsforaccount"    -> Indica cuantos campos se requiere que coincidan para garantizar el acceso (los valores son 1 o 2 campos)
"cleanerrors"         -> Si estas tan loco como yo esto te permite eliminar toda la informacion en caso de x cantidad de errores en credenciales (0=Desactivado, desde
1 en adelante pueden poner la cantidad de intentos que deseen) (ASEGURATE DE SABER LO QUE HACES)
