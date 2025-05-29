create table if not exists public.food_analysis_results (
  id uuid not null default gen_random_uuid (),
  user_id uuid not null,
  image_url text not null,
  food_name_en text not null,
  food_name_th text not null,
  created_at timestamp with time zone not null default (now() AT TIME ZONE 'utc'::text),
  deleted_at timestamp with time zone null,
  constraint food_analysis_results_pkey primary key (id),
  constraint food_analysis_results_user_id_fkey foreign KEY (user_id) references auth.users (id) on delete CASCADE
) TABLESPACE pg_default;

create table if not exists public.food_components (
  id uuid not null default gen_random_uuid (),
  far_id uuid not null,
  name_en text not null,
  name_th text not null,
  calories integer not null,
  protein integer not null,
  carbohydrates integer not null,
  fat integer not null,
  fiber integer not null,
  sugar integer not null,
  deleted_at timestamp with time zone null,
  constraint food_component_pkey primary key (id),
  constraint food_components_far_id_fkey foreign KEY (far_id) references food_analysis_results (id) on delete CASCADE
) TABLESPACE pg_default;

create index if not exists idx_far_user_id on food_analysis_results (user_id);
create index if not exists idx_far_user_created_at
  on food_analysis_results (user_id, created_at);
create index if not exists idx_fc_far_id on food_components (far_id);

CREATE OR REPLACE FUNCTION insert_food_analysis_with_components(
    _id UUID,
    _user_id UUID,
    _food_name_en TEXT,
    _food_name_th TEXT,
    _image_url TEXT,
    _created_at TIMESTAMPTZ,
    _food_components JSONB
) RETURNS VOID AS $$
DECLARE
    component JSONB;
BEGIN
    BEGIN
        INSERT INTO food_analysis_results (
            id,
            user_id,
            food_name_en,
            food_name_th,
            image_url,
            created_at,
            deleted_at
        ) VALUES (
            _id,
            _user_id,
            _food_name_en,
            _food_name_th,
            _image_url,
            _created_at,
            NULL
        );

        FOR component IN SELECT * FROM jsonb_array_elements(_food_components)
        LOOP
            INSERT INTO food_components (
                id,
                far_id,
                name_en,
                name_th,
                calories,
                protein,
                carbohydrates,
                fat,
                fiber,
                sugar,
                deleted_at
            ) VALUES (
                (component ->> 'id')::UUID,
                _id,
                component ->> 'name_en',
                component ->> 'name_th',
                (component ->> 'calories')::INT,
                (component ->> 'protein')::INT,
                (component ->> 'carbohydrates')::INT,
                (component ->> 'fat')::INT,
                (component ->> 'fiber')::INT,
                (component ->> 'sugar')::INT,
                NULL
            );
        END LOOP;

    EXCEPTION
        WHEN OTHERS THEN
            RAISE;
    END;
END;
$$ LANGUAGE plpgsql;

create or replace function get_food_analysis_result(p_id uuid)
returns jsonb
language sql
as $$
with base as (
  select
    far.id as far_id,
    far.user_id,
    far.food_name_en,
    far.food_name_th,
    far.image_url,
    fc.id as component_id,
    fc.name_en,
    fc.name_th,
    fc.calories,
    fc.protein,
    fc.carbohydrates,
    fc.fat,
    fc.fiber,
    fc.sugar
  from food_analysis_results far
  left join food_components fc on fc.far_id = far.id and fc.deleted_at is null
  where far.id = p_id and far.deleted_at is null
),
aggregated as (
  select
    far_id,
    jsonb_agg(jsonb_build_object(
      'id', component_id,
      'name_en', name_en,
      'name_th', name_th,
      'calories', calories,
      'protein', protein,
      'carbohydrates', carbohydrates,
      'fat', fat,
      'fiber', fiber,
      'sugar', sugar
    )) as food_components,
    coalesce(sum(calories), 0) as total_calories,
    coalesce(sum(protein), 0) as total_protein,
    coalesce(sum(carbohydrates), 0) as total_carbohydrates,
    coalesce(sum(fat), 0) as total_fat,
    coalesce(sum(fiber), 0) as total_fiber,
    coalesce(sum(sugar), 0) as total_sugar
  from base
  group by far_id
)
select jsonb_build_object(
  'id', far.id,
  'user_id', far.user_id,
  'food_name_en', far.food_name_en,
  'food_name_th', far.food_name_th,
  'image_url', far.image_url,
  'food_components', agg.food_components,
  'total_calories', agg.total_calories,
  'total_protein', agg.total_protein,
  'total_carbohydrates', agg.total_carbohydrates,
  'total_fat', agg.total_fat,
  'total_fiber', agg.total_fiber,
  'total_sugar', agg.total_sugar,
  'created_at', far.created_at
)
from food_analysis_results far
join aggregated agg on agg.far_id = far.id
where far.id = p_id and far.deleted_at is null;
$$;

create or replace function get_food_analysis_results_by_user(p_user_id uuid)
returns jsonb
language sql
as $$
with base as (
  select
    far.id as far_id,
    far.user_id,
    far.food_name_en,
    far.food_name_th,
    far.image_url,
    fc.id as component_id,
    fc.name_en,
    fc.name_th,
    fc.calories,
    fc.protein,
    fc.carbohydrates,
    fc.fat,
    fc.fiber,
    fc.sugar
  from food_analysis_results far
  left join food_components fc on fc.far_id = far.id and fc.deleted_at is null
  where far.user_id = p_user_id and far.deleted_at is null
),
aggregated as (
  select
    far_id,
    jsonb_agg(jsonb_build_object(
      'id', component_id,
      'name_en', name_en,
      'name_th', name_th,
      'calories', calories,
      'protein', protein,
      'carbohydrates', carbohydrates,
      'fat', fat,
      'fiber', fiber,
      'sugar', sugar
    )) as food_components,
    coalesce(sum(calories), 0) as total_calories,
    coalesce(sum(protein), 0) as total_protein,
    coalesce(sum(carbohydrates), 0) as total_carbohydrates,
    coalesce(sum(fat), 0) as total_fat,
    coalesce(sum(fiber), 0) as total_fiber,
    coalesce(sum(sugar), 0) as total_sugar
  from base
  group by far_id
),
final_data as (
  select
    far.id,
    far.user_id,
    far.food_name_en,
    far.food_name_th,
    far.image_url,
    far.created_at,
    agg.food_components,
    agg.total_calories,
    agg.total_protein,
    agg.total_carbohydrates,
    agg.total_fat,
    agg.total_fiber,
    agg.total_sugar
  from food_analysis_results far
  join aggregated agg on agg.far_id = far.id
  where far.user_id = p_user_id and far.deleted_at is null
)
select jsonb_agg(jsonb_build_object(
  'id', id,
  'user_id', user_id,
  'food_name_en', food_name_en,
  'food_name_th', food_name_th,
  'image_url', image_url,
  'food_components', food_components,
  'total_calories', total_calories,
  'total_protein', total_protein,
  'total_carbohydrates', total_carbohydrates,
  'total_fat', total_fat,
  'total_fiber', total_fiber,
  'total_sugar', total_sugar,
  'created_at', created_at
))
from final_data;
$$;

create or replace function get_food_analysis_results_by_user_and_date(
  p_user_id uuid,
  p_start_date timestamptz,
  p_end_date timestamptz
)
returns jsonb
language sql
as $$
with base as (
  select
    far.id as far_id,
    far.user_id,
    far.food_name_en,
    far.food_name_th,
    far.image_url,
    far.created_at,
    fc.id as component_id,
    fc.name_en,
    fc.name_th,
    fc.calories,
    fc.protein,
    fc.carbohydrates,
    fc.fat,
    fc.fiber,
    fc.sugar
  from food_analysis_results far
  left join food_components fc on fc.far_id = far.id and fc.deleted_at is null
  where far.user_id = p_user_id
    and far.created_at >= p_start_date
    and far.created_at <= p_end_date
    and far.deleted_at is null
),
aggregated as (
  select
    far_id,
    jsonb_agg(jsonb_build_object(
      'id', component_id,
      'name_en', name_en,
      'name_th', name_th,
      'calories', calories,
      'protein', protein,
      'carbohydrates', carbohydrates,
      'fat', fat,
      'fiber', fiber,
      'sugar', sugar
    )) as food_components,
    coalesce(sum(calories), 0) as total_calories,
    coalesce(sum(protein), 0) as total_protein,
    coalesce(sum(carbohydrates), 0) as total_carbohydrates,
    coalesce(sum(fat), 0) as total_fat,
    coalesce(sum(fiber), 0) as total_fiber,
    coalesce(sum(sugar), 0) as total_sugar
  from base
  group by far_id
),
final_data as (
  select
    far.id,
    far.user_id,
    far.food_name_en,
    far.food_name_th,
    far.image_url,
    far.created_at,
    agg.food_components,
    agg.total_calories,
    agg.total_protein,
    agg.total_carbohydrates,
    agg.total_fat,
    agg.total_fiber,
    agg.total_sugar
  from food_analysis_results far
  join aggregated agg on agg.far_id = far.id
  where far.user_id = p_user_id
    and far.created_at >= p_start_date
    and far.created_at <= p_end_date
    and far.deleted_at is null
)
select jsonb_agg(jsonb_build_object(
  'id', id,
  'user_id', user_id,
  'food_name_en', food_name_en,
  'food_name_th', food_name_th,
  'image_url', image_url,
  'created_at', created_at,
  'food_components', food_components,
  'total_calories', total_calories,
  'total_protein', total_protein,
  'total_carbohydrates', total_carbohydrates,
  'total_fat', total_fat,
  'total_fiber', total_fiber,
  'total_sugar', total_sugar
))
from final_data;
$$;

