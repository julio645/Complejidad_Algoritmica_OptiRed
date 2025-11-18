<div align="center">
  
  ## **Universidad Peruana de Ciencias Aplicadas**

  ## **Complejidad Algorítmica**
  
  ## **Informe de Trabajo Parcial \- Segundo Hito**
  
  ## **Profesor:**  
  **Arias Orihuela John Edward**
  
  ## **Sección:**
  **1416**
  
  ## **Integrantes:**  
  **Blancas Chavez, Carlos Franco**   
  **Celis Berrospi, Eslander**   
  **Guillen Galindo, Julio Adolfo**
</div>

- # **Descripción del problema:**

Lima, la capital del Perú, es una ciudad con más de 10 millones de habitantes y una geografía urbana compleja que incluye distritos céntricos y zonas periféricas. A pesar de ser el centro principal de infraestructura de telecomunicaciones del país, la cobertura de señal telefónica móvil, especialmente en tecnologías 4G, no es homogénea en toda la ciudad (OSIPTEL, s.f.). Existen zonas donde la señal es débil o inexistente, lo que afecta la calidad del servicio y limita el acceso a comunicaciones esenciales para la vida diaria, el trabajo y la educación.

Esta desigualdad se debe principalmente a la distribución desigual de antenas. Las operadoras como Claro (América Móvil Perú), Entel (Entel Perú), Movistar(Telefónica del Perú) y Bitel (Viettel Perú), concentran sus antenas en distritos con mayor rentabilidad económica, dejando zonas periféricas con poca infraestructura. En distritos densamente poblados, pocas antenas deben soportar una gran cantidad de usuarios, lo que genera saturación, disminución de velocidad y desconexiones frecuentes. Además, factores como la topografía y la presencia de edificios altos dificultan la propagación de la señal, creando “puntos muertos” en la ciudad (MTC, s. f.).

Esta situación impacta negativamente en la calidad de vida de los usuarios, limitando el acceso a servicios digitales, afectando la productividad laboral y la educación en línea, especialmente en zonas vulnerables. Por ejemplo, en distritos periféricos, muchos usuarios experimentan velocidades inferiores a 5 Mbps y latencias elevadas, lo que dificulta el uso de aplicaciones básicas (Presidencia del Consejo de Ministros, s. f.)..

Una solución práctica para mitigar este problema es que los usuarios elijan la empresa de telecomunicaciones que ofrece la mejor cobertura y calidad de señal en su ubicación específica. Promover esta selección basada en datos reales ayuda a mejorar la experiencia del usuario y fomenta la competencia entre operadoras para ampliar y mejorar su infraestructura en zonas menos atendidas. Así, se contribuye a reducir la brecha digital en Lima y a garantizar un acceso más equitativo a los servicios de telecomunicaciones (OSIPTEL, s. f).

En este contexto, la red de antenas puede representarse mediante un grafo, donde los nodos representan antenas y las aristas representan enlaces posibles entre ellas. El peso de cada arista podría corresponder a la distancia. Aplicando algoritmos de Kruskal, se puede determinar la mejor ruta o conexión para ampliar la cobertura de señal hacia zonas con baja conectividad.

- # **Descripción del conjunto de datos (dataset):**

Este proyecto emplea un dataset proveniente del Portal de Datos Abiertos del Gobierno del Perú, titulado “Cobertura de servicio móvil por empresa operadora”, publicado por el Ministerio de Transportes y Comunicaciones (MTC). La elección de este conjunto de datos se debe a su relevancia como fuente pública y oficial, que recopila información actualizada sobre la cobertura del servicio móvil en todo el territorio nacional. Este recurso constituye un insumo fundamental para modelar redes de telecomunicaciones y analizar la expansión de infraestructura mediante el uso de grafos.

El dataset está organizado donde cada fila representa un centro poblado con cobertura móvil declarada por una empresa operadora, mientras que cada columna describe atributos geográficos y técnicos del servicio. Esta estructura permite representar las relaciones espaciales y tecnológicas entre los distintos puntos de cobertura en el país.

El archivo descargado contiene un extenso conjunto de registros con múltiples variables (más de 20), de las cuales en este proyecto se seleccionarán las más relevantes para el modelado de la red:

* **DEPARTAMENTO / PROVINCIA / DISTRITO:** Ubicación geográfica del centro poblado.  
* **CENTRO\_POBLADO:** Nombre del lugar con cobertura móvil.  
* **LATITUD / LONGITUD:** Coordenadas geográficas del punto de cobertura.  
* **EMPRESA\_OPERADORA:** Nombre de la empresa que brinda el servicio.  
* **TECNOLOGÍA (2G, 3G, 4G, 5G):** Tipo de red móvil disponible.  
* **CANT\_EB\_2G / CANT\_EB\_3G / CANT\_EB\_4G / CANT\_EB\_5G:** Cantidad de estaciones base que brindan cobertura con cada tecnología.

En este caso, cada nodo del grafo representará un centro poblado con cobertura móvil, identificado por su nombre y coordenadas geográficas, las aristas conectan los nodos que se encuentren a una distancia viable para un enlace de fibra óptica, y su peso se determinará en función de la distancia geográfica o del costo estimado de instalación del enlace entre ambas ubicaciones.  
Esta representación gráfica permite visualizar y analizar los 1500 nodos de la infraestructura móvil nacional de manera más eficiente, identificando las rutas óptimas para la expansión de cobertura, los puntos críticos sin conexión y las oportunidades de optimización del despliegue de red. Así, el grafo no solo cumple una función representativa, sino que se convierte en una herramienta analítica estratégica que facilita la planificación y toma de decisiones en el ámbito de las telecomunicaciones.  
![][image1]

- # **Propuesta:**

El objetivo de la propuesta es desarrollar un modelo basado en grafos que permita encontrar las rutas más eficientes para interconectar antenas de telecomunicaciones entre distritos, considerando restricciones de distancia máxima y compatibilidad tecnológica (por ejemplo, que compartan al menos una generación de red: 3G, 4G o 5G).

**¿Quién necesita esta propuesta?**

* Empresas de telecomunicaciones (Movistar, Claro, Entel, Bitel): podrán planificar la expansión de sus redes al menor costo posible, priorizando la reutilización de infraestructura existente.  
* El Estado (MTC, PRONATEL): para diseñar proyectos de conectividad rural que aseguren que cada distrito quede integrado en la red nacional. De acuerdo con el Ministerio de Transportes y Comunicaciones, más del 30 % de los hogares rurales aún no tiene acceso a Internet, lo que refleja la magnitud de la brecha digital (MTC, 2023).

**Técnica y metodología a utilizar:**

1. Modelado del grafo:  
* Cada antena principal en un centro poblado será un nodo con su latitud y longitud.  
* Se establecerán aristas solo entre antenas que:  
  * Estén dentro de una distancia máxima (10 km).  
  * Compartan al menos una generación de red (3G, 4G o 5G).  
* Se garantizará que al menos una antena de cada distrito se conecte a otro distrito, evitando grafos aislados, como recomiendan los proyectos de interconexión regional impulsados por PRONATEL (PRONATEL, 2024).

2. Algoritmos de búsqueda y optimización:  
* Kruskal o Prim: para construir la red de costo mínimo conectando todos los nodos sin dejar distritos aislados.

3. Resultados esperados:  
* Una red optimizada que muestre la mejor manera de interconectar distritos.  
* Reducción de costos de instalación al aprovechar la infraestructura ya existente.  
* Mayor cobertura digital en zonas rurales, donde más de 3 millones de personas aún no cuentan con Internet (Infobae, 2024).


- # **Diseño del aplicativo:**

(Hito 2\)

- # **Validación de resultados y pruebas:**

(Hito 3\)

- # **Conclusiones:**

(Hito 3\)

- # **Referencias bibliográficas:**

1. Presidencia del Consejo de Ministros. (s. f.). *Plataforma Nacional de Datos Abiertos*. [https://datosabiertos.gob.pe/](https://datosabiertos.gob.pe/)    
2. Osiptel. (s. f.). *Osiptel-COM Edición 03*. Repositorio Osiptel. [https://repositorio.osiptel.gob.pe/bitstream/handle/20.500.12630/646/osiptel-com-edicion03.pdf?sequence=1\&isAllowed=y](https://repositorio.osiptel.gob.pe/bitstream/handle/20.500.12630/646/osiptel-com-edicion03.pdf?sequence=1&isAllowed=y)    
3. Ministerio de Transportes y Comunicaciones. (s. f.). *MTC trabaja para promover conectividad en infraestructura en telecomunicaciones a fin de reducir brecha digital en zonas. rurales*. [https://www.gob.pe/institucion/mtc/noticias/949594-mtc-trabaja-para-promover-conectividad-en-infraestructura-en-telecomunicaciones-a-fin-de-reducir-brecha-digital-en-zonas-rurales](https://www.gob.pe/institucion/mtc/noticias/949594-mtc-trabaja-para-promover-conectividad-en-infraestructura-en-telecomunicaciones-a-fin-de-reducir-brecha-digital-en-zonas-rurales)   
4. Banco Interamericano de Desarrollo. (2022). Informe sobre la situación de conectividad de Internet y banda ancha en Perú. [https://publications.iadb.org/publications/spanish/document/Informe-sobre-la-situaci%C3%B3n-de-conectividad-de-Internet-y-banda-ancha-en-Per%C3%BA.pdf](https://publications.iadb.org/publications/spanish/document/Informe-sobre-la-situaci%C3%B3n-de-conectividad-de-Internet-y-banda-ancha-en-Per%C3%BA.pdf)  
5. Infobae. (2024, octubre 24). Más de 3 millones de peruanos ni siquiera tienen acceso a internet: brecha de telefonía móvil todavía llega al 40%. [https://www.infobae.com/peru/2024/10/24/mas-de-3-millones-de-peruanos-ni-siquiera-tienen-acceso-a-internet-brecha-de-telefonia-movil-todavia-llega-al-40/](https://www.infobae.com/peru/2024/10/24/mas-de-3-millones-de-peruanos-ni-siquiera-tienen-acceso-a-internet-brecha-de-telefonia-movil-todavia-llega-al-40/)   
6. Ministerio de Transportes y Comunicaciones. (2023). MTC presenta propuestas técnicas para reducir la brecha de conectividad en zonas rurales del país. [https://www.gob.pe/institucion/mtc/noticias/812868-mtc-presenta-propuestas-tecnicas-para-reducir-la-brecha-de-conectividad-en-zonas-rurales-del-pais](https://www.gob.pe/institucion/mtc/noticias/812868-mtc-presenta-propuestas-tecnicas-para-reducir-la-brecha-de-conectividad-en-zonas-rurales-del-pais)   
7. Programa Nacional de Telecomunicaciones. (2024). PRONATEL ejecutará 8 proyectos de banda ancha en Perú. [https://dplnews.com/pronatel-ejecutara-8-proyectos-de-banda-ancha-en-peru](https://dplnews.com/pronatel-ejecutara-8-proyectos-de-banda-ancha-en-peru) 

[image1]:
