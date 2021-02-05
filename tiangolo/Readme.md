
# Running a tiangolo image non-root
 
On starting the lint trilogy project, I decided for a containerized web server with python support. 
Looking around, I found the tiangolo/uwsgi-nginx-flask image very handy and so I started building
my application on top of it.

As long as I worked on a plain Rancher Kubernetes cluster, everything was fine. But when I changed
to an OpenShift cluster, trouble came around the corner. The container wouldn't start, complaining
it couldn't create /etc/nginx/nginx.conf.
 
The full error message:
```
/uwsgi-nginx-entrypoint.sh: 45: /uwsgi-nginx-entrypoint.sh: cannot create /etc/nginx/nginx.conf: Permission denied
```

The tiangolo image relies on running as root user, which OpenShift does not supply in the default configuration.
At first sight this seemed to make the image unusable for my purposes. But after fiddling around a bit, I worked out
two solutions to let my application run with the uwsgi-nginx-flask image on OpenShift/OKD:

* Create a serviceAccount with the anyuid policy in OpenShift/OKD and use this in the
security context of the deployment
* Build your own image based on tiangolo/uwsgi-nginx-flask to make it able to run as non-root user.

## Running tiangolo/uwsgi-nginx-flask with a serviceAccount

Create a serviceAccount in OpenShift and assign the policy _anyuid_  to it. You need extended rights to do
this in OCP/OKD, which means in most cases you need to be (cluster) admin. Example:
```
# create service account
oc create sa my-sa-with-anyuid

# allow the account to run things with any uid
oc adm policy add-scc-to-user anyuid -z my-sa-with-anyuid
```
Once created, extend the deployment witrh a security context and use the new serviceAccount
in that. Example:
```
  ...
    spec:
      securityContext:
        fsGroup: 0
      serviceAccount: my-sa-with-anyuid
      serviceAccountName: my-sa-with-anyuid

      containers:
        - name: tiangolo-with-sa
          image: tiangolo/uwsgi-nginx-flask:python3.8
          ports:
            - containerPort: 80
```

This lets the container run as root user, as you can see when running _id_ on a shell inside the container:
```
bash inside # id
uid=0(root) gid=0(root) groups=0(root)
bash inside #
```

After deploying the exampe file with-sa/deployment.yaml the container opens port 80 and is accessible via
a service which is deployed with the pod. Try to access it from another pod with a simple curl:
```
bash # curl http://tiangolo-with-sa.yournamespace.svc.cluster.local
Hello World from Flask in a uWSGI Nginx Docker container with Python 3.8 (default)
bash #
```
Pro:
* no need to build an onw image based on tiangolo

Cons:
* you need the right to create a service account. Or need to know somebody who owns those rights and owes you a favor.

Find more information about service accounts in the [OpenShift documentation](https://www.openshift.com/blog/a-guide-to-openshift-and-uids).

## Enhancing the tiangolo/uwsgi-nginx-flask image

If you don't have the possibility to create a service account but still want or need to run a container based on 
the uwsgi-nginx-flask image, then you need to build your own image, based on the tiangolo version and doing
some "enhancements".
* Change the web servers port to 8080 (or another one >1023).
* Modify some configuration files
* Make some files writable to the root group (gid=0)
The main trick is that OpenShift/OKD denies the pods to run as root user, but allows them to run as group root.

### Change the tcp port
By default the webserver tries to open port 80 which needs root privileges. Therefore this example chooseds
port 8080 for communication. This needs to be set in the _dockerfile_:
```
ENV LISTEN_PORT 8080
EXPOSE          8080
```
The environment variable LISTEN_PORT is used inside the container to configure the port for the web server. 
This is a standard feature of the tiangolo/uwsgi-nginx-flask image.

### Change uwsgi.conf
Additionally, you need to modify uwsgi.con, means create a new one and overwrite the original one.
The following section is important:
```
[uwsgi]
socket = /tmp/uwsgi.sock
chmod-socket = 660
```
This makes the needed socket writable to the root group which is the trick in this case. The uwsgi.ini is copied into
the images filesystem together with an adapted supervisord.conf.

### Make some files & directories writable
Furthermore, it's needed to make some files and directories writeable to the root group. This is mainly
the nginx configuration and some log directories. This is done in the dockerfile, right after copying the
modified config files:
```
RUN  echo  "Start building on top of tiangolo image ..." \
 &&  cp /app/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf \
 &&  cp /app/conf/uwsgi.ini        /app/uwsgi.ini    \
 &&  touch /etc/nginx/conf.d/nginx.conf \
 &&  chmod -R g+rwx /var/log/supervisor \
 &&  chmod -R g+rwx /var/cache/nginx /var/run /var/log/nginx  /etc/nginx/
```

Now build the image and push it to your registry:
```
docker build -t myrepo/tiangolo-enhcd:0.1.0  .
docker push     myrepo/tiangolo-enhcd:0.1.0
```



