from datetime import datetime, timedelta

import pytest

pytest.mark.integration


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_enabled(incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    job_ids = [j.id for j in scheduler.get_jobs()]
    assert incoming_webhook.job_id in job_ids


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_disabled(
        incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    incoming_webhook.enabled = False
    incoming_webhook.save()
    job_ids = [j.id for j in scheduler.get_jobs()]
    assert incoming_webhook.job_id not in job_ids


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_reschedule_crontab(
        incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    old_job_id = incoming_webhook.job_id
    now = datetime.now()
    future_time = now + timedelta(minutes=15)
    incoming_webhook.crontab = '{} * * * *'.format(future_time.minute)
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    assert incoming_webhook.job_id != old_job_id


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_reschedule_stale(
        incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    old_job_id = incoming_webhook.job_id
    scheduler.cancel(incoming_webhook.job_id)
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    assert incoming_webhook.job_id != old_job_id


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_remove_orphan_job_id(
        incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    scheduler.cancel(incoming_webhook.job_id)
    incoming_webhook.enabled = False
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    assert incoming_webhook.job_id == ''


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_no_repeat(
        incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.id == incoming_webhook.job_id:
            repeat = job.meta['repeat']
    assert repeat == 0


@pytest.mark.django_db
def test_handle_incoming_webhook_schedule_repeat(
        incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.repeat = True
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.id == incoming_webhook.job_id:
            job = job
    assert hasattr(job.meta, 'repeat') is False


@pytest.mark.django_db
def test_cancel_incoming_webhook_schedule(incoming_webhook, scheduler):
    incoming_webhook.enabled = True
    incoming_webhook.save()
    incoming_webhook.refresh_from_db()
    incoming_webhook.delete()
    job_ids = [j.id for j in scheduler.get_jobs()]
    assert incoming_webhook.job_id not in job_ids
