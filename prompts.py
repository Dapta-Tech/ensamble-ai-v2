prompt_1_Introduccion = """
Tu tarea es {question} para el documento piscc 2024.

Esta sección esta basada en delitos para el municipio de: {municipio}
Siguiendo el siguiente contexto:{context} para identificar todos los factores de riesgo que pueden conllevar 
a delitos en el municipio.

Basa el documento en la información de delitos de los ultimos 5 años del municipio {municipio}
detallado en la siguiente sección: {delitos_mes_a_mes}

Para la redacción de la sección 1. debes tomar los siguientes puntos:
- Describe de manera general los retos frente delitos mas frecuentes la ultima temporada.
- Para qué servirá el piscc en el municipio de {municipio}.
- ¿Cuál es el compromiso la realización del piscc 2024-2027?
- ¿Cuál será el resultado del proceso?

Sobre el formato:
- Incluye el uso de negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.
- Establece Objetivo general y Objetivos específicos basados en los delitos de manera general y el contexto.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos largos.
- No incluyas un párrafo de resumen de la sección.

Redacta solo la Sección 1. Introducción en formato HTML:
"""

prompt_2_Introduccion = """
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

Esta se enfoca en el marco legislativo que respalda la creación de PISCC y su objetivo,
Siguiendo el siguiente contexto:{context}, cita las leyes de importancia para programa
el plan integral de ocnvivencia y seguridad ciduadana.

Toma en cuneta los delitos de los ultimos 5 años del municipio {municipio} 
detallado en la siguiente sección: {delitos_mes_a_mes} par avalidar el marco normativo.

Para la redacción de la sección 2. debes tomar los siguientes puntos:
- Lineamiento del Plan Nacional de Desarrollo del Gobierno nacional co nel piscc.
- Incluye enfoques diferenciales e interseccionales según las características y necesidades de la 
población en la entidad territorial segun  la información de:
    - Características geográficas de {municipio}
    - Demografía de {municipio}

Sobre el formato:
- Incluye el uso de negritas, cursivas para ayudar al lector a identificar los puntos clave.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos largos.
- No incluyas un párrafo de resumen de la sección.

Redacta solo la Sección 2. en formato HTML:
"""
#Se recomienda contar con el detalle del municipio para datos de género o información de 
#la comunidad LGBTQ+ en el municipio.

prompt_3_Diagnostico = """
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

Esta sección esta basada en la introducción a datos sobre el municipio de: {municipio}
Siguiendo el siguiente contexto:{context} describe la información del municipio, del alcalde y sus
principales funciones y resposnabilidad en la elaboración del piscc.

Describe los delitos de manera general en un solo parrafo: {delitos_mes_a_mes}.

Sobre el formato:
- Incluye el uso de negritas al lector a identificar los puntos clave.
- El nombre de la sección es "3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana"

IMPORTANTE: 
- El documento generado debe tener un mínimo de 5 párrafos largos.
- No incluyas un párrafo de resumen de la sección.

Redacta solo la Sección 3 en formato HTML:
"""
#¿Cómo saber cuál es el alcalde alctual de cada municipio?

prompt_3_1_Diagnostico = """
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

Esta sección esta basada en delitos para el municipio de: {municipio}
Siguiendo el siguiente contexto:{context} para identificar todos los factores de riesgo que pueden conllevar 
a delitos en el municipio.

Basa el documento en la información de delitos de los ultimos 5 años del municipio {municipio}
detallado en la siguiente sección: {delitos_mes_a_mes}

Para la redacción de la sección 3.1 se debe redactar la directa relación de violencia y delitos 
descritos con los siguientes puntos:
- Características geográficas de {municipio}
- Demografía de {municipio}
- Actividades económicas de {municipio}
- Infraestructura de {municipio}
- Instituciones y organizaciones de {municipio}
- Seguridad ciudadana de {municipio}
- Justicia: se sugiere incorporar la capacidad de la Comisaría de Familia, vehículos con los que cuenta,
infraestructura, equipos disponibles para las entidades que hacen parte de esta categoría. para el municipio de {municipio}

Sobre el formato:
- No incluyas un párrafo de resumen de la sección.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos largos.

Redacta solo la Sección 3.1 Análisis de Estadísticas de Seguridad en formato HTML:
"""

prompt_3_2_Diagnostico ="""
Tu tarea es {question} para el documento piscc 2024 enlazando la sección previa: {seccion_context}.

La sección 3.2 del municipio: {municipio} Sigue el siguiente contexto:{context}
Tomando en cuenta los delitos registrados: {delitos_mes_a_mes} la seccion se redacta siguiendo los siguientes puntos:
1. Información general del municipio {municipio}.
2. Antecedentes históricos del municipio {municipio} que hayan impactado los temas de acceso a la justicia.
3. Análisis del contexto territorial (población, calidad de vida, condiciones económicas y políticas, entre 
otras).
4. Análisis de conflictividad del municipio {municipio} (causas y efectos de las conflictividades, barreras de 
acceso a la justicia, tipologías de conflicto, entre otros).
5. Mapeo de actores (organizaciones comunitarias, oferta de justicia y convivencia, entidades del 
orden local, entre otros).

Sobre el formato:
- Incluye el uso de negritas y cursivas para ayudar al lector a identificar los puntos clave.
- No incluyas un párrafo de resumen de la sección.

IMPORTANTE: El documento generado debe tener un mínimo de 10 párrafos largos.
Redacta 3.2 Diagnóstico de conflictividades. en formato HTML:
"""

prompt_3_3_Diagnostico ="""
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 3.3 del municipio: {municipio} Sigue el siguiente contexto:{context}

la seccion se redacta siguiendo los siguientes puntos:
- Principales comportamientos contrarios a la convivencia. 
- Número y tipo de comportamientos contrarios a la convivencia que afectan a personas de 
determinados grupos étnicos, así como a personas con orientaciones sexuales e identidades de género diversas.

Sobre el formato:
- Incluye el uso de negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.

IMPORTANTE: 
- No incluyas un párrafo de resumen de la sección.
- Incluye 3 párrafos para cada sección.

Redacta 3.3 Diagnóstico de comportamientos contrarios a la convivencia. en formato HTML:
"""

prompt_3_4_Diagnostico ="""
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 3.4 del municipio: {municipio} Sigue el siguiente contexto:{context}

La seccion se redacta siguiendo los siguientes puntos:
- Número y tipo de comportamientos contrarios a la convivencia que afectan a personas de 
determinados grupos étnicos, así como a personas con orientaciones sexuales e identidades de género diversas.
- Detalle estadístico minucioso sobre los delitos en el municipio de {municipio} en los últimos 
5 años detallados en la sección: {delitos_mes_a_mes}.


IMPORTANTE: 
- El documento generado debe tener un mínimo de 20 párrafos largos.
- No incluyas un párrafo de resumen de la sección.

Redacta 3.4 Diagnóstico de delitos. en formato HTML:
"""
#Integrar tpcmh
#Integrar grupos étnicos
#Comunidad LGBTQ+

prompt_4_Focalizacion ="""
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 4 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
4. Focalización y Priorización para la Planeación
4.1 Identificación de Zonas Críticas
4.2 Definición de Grupos de Población Vulnerables
4.3 Priorización de Problemas a Abordar

La sección se basa en los delitos: {delitos_mes_a_mes} en los últimos 5 años. y a partir de estos definiendo:
- Selecición de los 3 delitos más frecuentes en el municipio de {municipio} los últimos 3 años.
- Criterios que se utilizaron para seleccionar las problematicas (delitos).
- Marco legal que respalda la focalización y priorización de los delitos.

Sobre el formato:
- Incluye un poco de negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.
- Incluye una tabla donde se idnetifiquen los 3 delitos seleccionados y los puntos de selección de cada uno asignando un puntaje de 1 a 10
según los puntos extraídos de las politicas extraidas del contexto: {context}.
- Incluye las estrategias de manera general de intervención para cada uno de los delitos seleccionados que se mencionan en el contexto.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 20 párrafos largos.
- No incluyas un párrafo de resumen de la sección.

Redacta parafos extensos de las secciones en formato HTML:
"""

prompt_5_Formulacion = """ 
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 5 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
5. Formulación Estratégica del PISCC
5.1 Estrategias de Intervención

La sección se basa en los delitos seleccionados en {seccion_context} de los delitos detallados el {delitos_mes_a_mes},
a partir estos detalla lo siguiente::
- Detalle de cada estrategias de intervención para cada uno de los delitos seleccionados.
- Justificación de la selección de las estrategias de intervención.
- Relación de las estrategias de intervención con los objetivos del PISCC.
- Relación de las estrategias de intervención con los resultados esperados del PISCC.
- Relación de las estrategias de intervención con los indicadores de gestión y resultados del PISCC.

Sobre el formato:
- Incluye cursivas para ayudar al lector a identificar los puntos clave.
- Incluye la justificación de responsabilidad del alcalde en la implementación de las estrategias de intervención.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones

Redacta parafos extensos de las secciones en formato HTML:
"""

prompt_6_Financiamiento = """ 
Tu tarea es {question} para el documento piscc 2024 continuando a la sección previa: {seccion_context}.

La sección 6 del municipio: {municipio} Sigue el siguiente contexto:{context} para la
redacción de los siguientes puntos:
6. Planeación Financiera y Operativa
6.1 Presupuesto Estimado
6.2 Recursos Necesarios
6.3 Asignación de Responsabilidades

La sección se basa en los delitos seleccionados en {seccion_context} de los delitos detallados el {delitos_mes_a_mes},
a partir estos detalla lo siguiente::
- Presupuesto estimado para la implementación de las estrategias de intervención.
- Recursos necesarios para la implementación de las estrategias de intervención.
- Asignación de responsabilidades para la implementación de las estrategias de intervención.

Sobre el formato:
- Incluye negritas, cursivas y listas para ayudar al lector a identificar los puntos clave.
- Incluye una tabla donde se haga un plan de división del presupuesto estimado para la implementación
de las estrategias de intervención de manera detallada.

IMPORTANTE: 
- El documento generado debe tener un mínimo de 10 párrafos extensos.
- No incluyas un párrafo de resumen de la sección.
- No aumentes otras secciones

Redacta parafos extensos para cada sección del punto 6 en formato HTML:
"""

prompt_7_Implementacion = """
"""

prompt_8_Seguimiento = """
"""

prompt_1_Introduccion
prompts_dict = { "1 Introducción": prompt_1_Introduccion,
                "2 Marco Normativo": prompt_2_Introduccion,
                "3 Diagnostico 3.1": prompt_3_1_Diagnostico, 
            "3 Diagnostico 3.2": prompt_3_2_Diagnostico,
            "3 Diagnostico 3.3": prompt_3_3_Diagnostico,
            "3 Diagnostico 3.4": prompt_3_4_Diagnostico,
            "4 Focalización" : prompt_4_Focalizacion,
            "5 Formulación" : prompt_5_Formulacion,
            "6 Financiamiento" : prompt_6_Financiamiento,
            "7 Implementación" : prompt_7_Implementacion,
            "8 Seguimiento" : prompt_8_Seguimiento}