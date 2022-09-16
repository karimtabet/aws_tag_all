import boto3
import botocore


class Tagger:
    def __init__(self, client=None, tags={}):
       self.client = client
       self.tags = tags
       self.resources = []
    
    def chunk_resources(self, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(self.resources), n):
            yield self.resources[i:i + n]
    
    def get_resources(self):
        """Get list of all resources"""
        response = self.client.get_resources(ResourcesPerPage=100)
        self.resources = response["ResourceTagMappingList"]
        while response["PaginationToken"]:
            response = self.client.get_resources(
                ResourcesPerPage=100,
                PaginationToken=response["PaginationToken"]
            )
            self.resources += response["ResourceTagMappingList"]

    def tag_resources(self):
        """Tag resources in chunks of 20"""
        chunked_resources = self.chunk_resources(20)
        for sub_list in chunked_resources:
            self.client.tag_resources(
                ResourceARNList=[r["ResourceARN"] for r in sub_list],
                Tags={'CostCentre': '509A0000'}
            )
    
    def tag_all(self):
        """For every available region, get all resources and tag them"""
        for region in boto3.session.Session().get_available_regions("ec2"):
            try:
                self.client = boto3.client('resourcegroupstaggingapi', region)
                self.get_resources()
                if self.resources:
                    self.tag_resources()
                    print(f"INFO: {region}: Tagged all resources")
                else:
                    print(f"INFO: {region}: No resources to tag")
            except botocore.exceptions.ClientError as e:
                print(f"WARNING: {region}: {str(e)}")
                continue
