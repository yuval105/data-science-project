((*- extends 'article.tplx' -*))

((* block maketitle *))

((*- if nb.metadata["latex_metadata"]: -*))
((*- if nb.metadata["latex_metadata"]["author"]: -*))
    \author{\normalsize ((( nb.metadata["latex_metadata"]["author"] )))}
((*- endif *))
((*- endif *))


((*- if nb.metadata["latex_metadata"]: -*))
((*- if nb.metadata["latex_metadata"]["title"]: -*))
    \title{((( nb.metadata["latex_metadata"]["title"] )))}
((*- endif *))
((*- else -*))
    \title{((( resources.metadata.name )))}
((*- endif *))

\date{\today}
\maketitle
((* endblock maketitle *))