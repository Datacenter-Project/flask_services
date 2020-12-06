#!/bin/sh

# Port forwarding for local development and tetsing
kubectl port-forward --address 0.0.0.0 service/elasticsearch 9200:9200 &
kubectl port-forward --address 0.0.0.0 service/broker 9092:9092 &
kubectl port-forward --address 0.0.0.0 service/broker 9101:9101 &
kubectl port-forward --address 0.0.0.0 service/zookeeper 2181:2181 &

