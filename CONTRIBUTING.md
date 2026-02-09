# Contribution Guidelines

Thank you for considering contributing to this project!

To ensure smooth collaboration, please follow these guidelines.

**We recommend joining our [Discord community](https://discord.gg/SgXCAQpTxy) to discuss your contributions.**

**Important Note:** You may need to generate test activities to validate your changes, which could incur costs on your GCP project. Please be aware of this before proceeding. If you're not comfortable with potential costs, consider discussing your changes on Discord first, and we will handle the testing for you.

## Mandatory Steps for Contribution

1. Fork the repository and create your branch from `main`
2. Install `mise`
3. Run `mise install` to set up the development environment
4. Enable a virtual environment (proposed by mise or manually)
5. Run `mise run i` to install all dependencies
6. Make your changes in your branch
7. Review [Generating Activities](#generating-activities) if your changes require test activities
8. Before submitting, ensure all tests pass by running `mise format`
9. Ensure your code achieves a PyLint rating of 10
10. Submit a pull request with a detailed description of your changes and the problem they solve

## Optional but Recommended Steps

- Write tests for your changes to ensure they work as expected
- Update documentation if your changes affect the usage or behavior of the project
- Engage in discussions on Discord to get feedback and suggestions from the community
- Use type hints in your Python code (not strictly required, but highly appreciated)

We appreciate your efforts to improve the project and look forward to reviewing your contributions!

## Adding a New Anti-Burst Object

ℹ️ **The term “Monitored Services” may be a slight misuse, as we monitor SKUs that are children of a “service.” This might be renamed later, but keep this in mind to avoid confusion.**

The project is designed to be extensible, and we’re especially interested in new **Anti-Burst Objects** that expand its capabilities. You don’t need to be a programmer to contribute here, as long as you can find the right metrics and pricing information to create a new object.

The goal is to create a combination of:
- Parent SKU
- SKU
- Related Metrics

This combination links metrics to their pricing and provides a complete picture of resource costs using Cloud Monitoring metrics, with billing estimates available in under 5 minutes.

Monitored Services objects are defined in `src/objects/monitored_services.py`. -> Understand the principle.

The Monitored Services list is available in `src/config/monitored_services_list.py`. -> Add new services here.


**References:**
- [Google Cloud SKU Documentation](https://cloud.google.com/skus)
- [Google Cloud Metrics List](https://cloud.google.com/monitoring/api/metrics_gcp)

Once you're comfortable with the functionality, feel free to add an Anti-Burst Object in `src/config/monitored_services.py`.

## Generating Activities

**Warning:** This may incur costs on your GCP project.

### Generating All Activities

To generate all activities, run the following command:

```bash
mise generate_activities
```

### Generating Specific Activities

#### Firestore

Generate the following activities:
- Firestore Read Activities
- Firestore Write Activities
- Firestore Delete Activities
- Firestore TTL Delete Activities (after 24 hours)

```bash
mise generate_firestore_activities
```

#### BigQuery

Run a BigQuery SELECT query on public datasets to generate activities (Billed Scanned Bytes):

```bash
mise generate_bigquery_activities
```

#### Gemini

List all Gemini models and perform a prediction request to each of them (Token input/output):

```bash
mise generate_gemini_activities
```

## Explore Anti Burst Objects

There is a script to help debug Cloud Billing and Cloud Monitoring data discrepancies:

```bash
mise test_objects
```

This will generate a `test_objects.json` at the root of the project. The file will contain detailed information about each Anti-Burst Object, including linked metrics and pricing data.

## Other Information

### Mise Tasks
Mise task scripts can be found in the `.mise-tasks` folder. Remember that adding new tasks may require running:

```bash
find .mise-tasks -type f -exec chmod +x {} \;
```

### Unit Tests

If you're looking to engage in an open source project, as this one lacks unit tests, you're more than welcome to had some!