"""
Customer Steps

Steps file for Customer.feature
"""
from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
import time

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '25'))

@given('the following customers')
def step_impl(context):
    """ Delete all Customers and load new ones """
    headers = {'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
    context.resp = requests.delete(context.base_url + '/customers/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
            "firstname": row['firstname'],
            "lastname": row['lastname'],
            "email": row['email'],
            "subscribed": row['subscribed'] in ['True', 'true', '1'],
            "address": {
                "address1": row['address1'],
                "address2": row['address2'],
                "city": row['city'],
                "province": row['province'],
                "country": row['country'],
                "zip": row['zip']
                }
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        if row['firstname'] == "John":
            tempdict = context.resp.json()
            context.john_id = tempdict["_id"]
        expect(context.resp.status_code).to_equal(201)

@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    context.resp = requests.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    # element = context.driver.find_element_by_id(element_id)
    # expect(element.get_attribute('value')).to_equal(text_string)
    time.sleep(5)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    time.sleep(5)
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element_by_id(element_id))
    expect(element.first_selected_option.text).to_equal(text)

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    time.sleep(5)
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)

@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    if element_name == "ID":
        text_string = context.john_id
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.send_keys(text_string)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower().replace(" ", "_") + '-btn'
    time.sleep(5)
    context.driver.find_element_by_id(button_id).click()
    time.sleep(2)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    element = context.driver.find_element_by_id(element_id)
    # element = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #     expected_conditions.presence_of_element_located((By.ID, element_id))
    # )
    element.clear()
    time.sleep(5)
    element.send_keys(text_string)

##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = 'customer_' + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)
