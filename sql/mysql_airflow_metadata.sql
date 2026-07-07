create table pipeline_runs (
  id varchar(64) primary key,
  dag_id varchar(128) not null,
  status varchar(32) not null,
  processed_rows int not null,
  created_at timestamp not null default current_timestamp
);

create index idx_pipeline_runs_dag_created
  on pipeline_runs(dag_id, created_at);
