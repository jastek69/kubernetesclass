    kubectl apply -f namespaces.yaml

https://github.com/BalericaAI/kubernetesclass/blob/main/datadog/yaml/namespace.yaml

    kubectl get ns --show-labels
    
    kubectl apply -f rbac.yaml

https://github.com/BalericaAI/kubernetesclass/blob/main/datadog/yaml/rbac.yaml

Test this:

    kubectl auth can-i get pods \
      --as system:serviceaccount:app01:jennifer \
      -n app01

  What happens?

  How about this?

      kubectl auth can-i delete deployments \
      --as system:serviceaccount:app01:jennifer \
      -n app01

  Why?

Let's check in on Chewy

    kubectl auth can-i create deployments \
      --as system:serviceaccount:app01:chewbacca \
      -n app01

How about Malgus

      kubectl auth can-i '*' '*' \
        --as system:serviceaccount:app01:malgus \
        -n app01

Why do we have these differences? 


  
  
