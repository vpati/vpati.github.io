FROM golang:alpine
ENV GOPATH=/go/
RUN apk add --no-cache --virtual git musl-dev
RUN git clone https://github.com/gohugoio/hugo.git /hugo
WORKDIR /hugo
RUN git checkout v0.51
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go install -ldflags '-s -w'

FROM alpine:latest
RUN apk add --no-cache git make
COPY --from=0 /go/bin/hugo /usr/bin
